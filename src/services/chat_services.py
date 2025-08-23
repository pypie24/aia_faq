import logging
import json
import uuid

from openai import OpenAI

from src.tools.client import chroma_client, llm_client, gemini_client
from src.config import settings

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

OPEN_AI_ROLE_MAPPING = {"human": "user", "ai": "assistant", "system": "system"}
GEMINI_AI_ROLE_MAPPING = {"human": "user", "ai": "model", "system": "model"}
DEFAULT_SEARCH_LIMIT = 5


class OpenAiClient:
    def __init__(self):
        self.client = llm_client
    
    def restructure_content(self, messages: list[dict]):
        new_message = []
        for message in messages:
            role = OPEN_AI_ROLE_MAPPING.get(message.get("role")) or "user"
            mes = {
                "role": role,
                "content": message.get("content")
            }
            new_message.append(mes)
        return new_message

    def chat(self, messages, model="gpt-4o-mini"):
        re_messages = self.restructure_content(messages)
        log.info(f"[openai message] {messages}")
        response = self.client.chat.completions.create(
            model=model,
            messages=re_messages,
            temperature=0.1
        )
        # Trả về thẳng string content thay vì object
        return response.choices[0].message.content


class GeminiClient:
    def __init__(self):
        self.client = gemini_client
    
    def restructure_content(self, messages: list[dict]):
        new_message = []
        for message in messages:
            role = GEMINI_AI_ROLE_MAPPING.get(message.get("role")) or "user"
            mes = {
                "role": role,
                "parts": [{"text": message.get("content")}]
            }
            new_message.append(mes)
        log.info(f"[gemini message] {new_message}")
        return new_message

    def chat(self, messages, model=settings.GEMINI_MODEL):
        re_messages = self.restructure_content(messages)
        response = self.client.models.generate_content(
            model=model,
            contents=re_messages,
            config={
                    "temperature": 0.1
                }
        )
        return response.text


llm = OpenAiClient()
gemini_llm = GeminiClient()


class RAG:
    def __init__(self, collection_name: str):
        self.collection = chroma_client.get_or_create_collection(name=collection_name)

    def _format_results(self, results: dict):
        """Chuyển kết quả từ ChromaDB thành dict dễ dùng."""
        if not results or not results.get("documents") or not results.get("metadatas"):
            return []

        docs_list = results["documents"][0]
        metas_list = results["metadatas"][0]
        ids_list = results["ids"][0] if "ids" in results and results["ids"] else [None]*len(docs_list)
        distances_list = results["distances"][0] if "distances" in results and results["distances"] else [0]*len(docs_list)

        formatted = []
        for i in range(len(docs_list)):
            meta = metas_list[i] if isinstance(metas_list[i], dict) else {}
            formatted.append({
                "_id": ids_list[i],
                "title": meta.get("title") or meta.get("name") or "N/A",
                "description": docs_list[i],
                "price": meta.get("price", "N/A"),
                "brand": meta.get("brand", "N/A"),
                "category": meta.get("tags", "N/A"),
                "distance": distances_list[i]
            })
        return formatted

    def vector_search(self, query_embedding: list, limit: int = DEFAULT_SEARCH_LIMIT):
        if not query_embedding:
            return []

        results_raw = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit
        )
        results = self._format_results(results_raw)
        log.debug(f"[DEBUG] Vector search results ({len(results)} items):")
        for r in results:
            log.debug(f"  {r['_id']}: {r['title']}, distance={r['distance']:.4f}")
        return results

    def keyword_search(self, query: str, limit=DEFAULT_SEARCH_LIMIT):
        """Tìm document dựa trên từ khóa text."""
        if not query:
            return []
 
        results_raw = self.collection.query(
            query_texts=[query],
            n_results=limit
        )
        results = self._format_results(results_raw)
        print(f"[DEBUG] Keyword search results ({len(results)} items):")
        for r in results:
            print(f"  {r['_id']}: {r['title']}, distance={r['distance']:.4f}")
        return results
 
    def reciprocal_rank_fusion(self, result_lists, k=3):
        """
        Kết hợp nhiều danh sách kết quả bằng Reciprocal Rank Fusion (RRF).
        result_lists: list các danh sách kết quả từ các search method.
        """
        scores = {}
        for results in result_lists:
            for rank, item in enumerate(results):
                doc_id = item["_id"]
                # RRF score
                score = 1.0 / (k + rank + 1)
                scores[doc_id] = scores.get(doc_id, 0) + score
 
        # Gom lại thông tin từ kết quả gốc (ưu tiên cái xuất hiện trước)
        id_to_doc = {}
        for results in result_lists:
            for item in results:
                if item["_id"] not in id_to_doc:
                    id_to_doc[item["_id"]] = item
 
        # Sort theo score
        fused = sorted(id_to_doc.values(), key=lambda x: scores.get(x["_id"], 0), reverse=True)
        return fused
 
    def hybrid_search(self, query_embedding: list, query_text: str = "", limit=DEFAULT_SEARCH_LIMIT):
        """
        Kết hợp vector search và keyword search, dùng RRF để fusion.
        query_embedding: vector embedding của câu hỏi
        query_text: text của câu hỏi
        """
        vector_results = self.vector_search(query_embedding, limit)
        keyword_results = self.keyword_search(query_text, limit) if query_text else []
        fused_results = self.reciprocal_rank_fusion([vector_results, keyword_results])
        print(f"[DEBUG] Hybrid search fused results ({len(fused_results)} items):")
        for r in fused_results[:limit]:
            print(f"  {r['_id']}: {r['title']}")
        return fused_results[:limit]

    def enhance_prompt(self, query_embedding: list):
        results = self.hybrid_search(query_embedding)
        if not results:
            log.debug("[DEBUG] No knowledge retrieved from RAG.")
            return ""

        prompt = "\n".join([
            f"Title: {r['title']}, Content: {r['description']}, Price: {r['price']}, Brand: {r['brand']}"
            for r in results
        ])
        return prompt


class Reflection:
    def __init__(self, chat_history_collection: str, semantic_cache_collection: str):
        self.history_collection = chroma_client.get_or_create_collection(name=chat_history_collection)
        self.semantic_cache_collection = chroma_client.get_or_create_collection(name=semantic_cache_collection)
    
    def raw_chat(self, messages):
        try:
            response_text = llm.chat(messages)
        except:
            response_text = gemini_llm.chat(messages)
        return response_text

    def chat(self, session_id: str, enhanced_message: str, original_message: str = '', cache_response: bool = False, query_embedding: list = None):
        # Build full prompt with context
        system_prompt_content = """
        Instruction:
        Bạn là chatbot cửa hàng bán điện thoại/laptop. Vai trò của bạn là hỗ trợ khách hàng trong việc tìm hiểu về các sản phẩm và dịch vụ của cửa hàng, cũng như tạo một trải nghiệm mua sắm dễ chịu và thân thiện.
        Hãy luôn giữ thái độ lịch sự và chuyên nghiệp. Nếu khách hàng hỏi về sản phẩm cụ thể, hãy cung cấp thông tin chi tiết và gợi ý các lựa chọn phù hợp. Nếu khách hàng trò chuyện về các chủ đề không liên quan đến sản phẩm, hãy tham gia vào cuộc trò chuyện một cách vui vẻ và thân thiện và đề xuất họ các thông tin về sản phẩm ví dụ: Bạn có quan tâm về điện thoại không?
        một số điểm chính bạn cần lưu ý:
        0. [Important] Chỉ trả lời dựa trên các thông tin của sản phẩm có trong database. Tuyệt đối không cung cấp thông tin bên ngoài hay gợi ý khách hàng tìm kiếm trên mạng.
        1. Đáp ứng nhanh chóng và chính xác, sử dụng xưng hô là "Mình và bạn".
        2. Giữ cho cuộc trò chuyện vui vẻ và thân thiện.
        3. Khi gặp những cầu hỏi còn lựa chọn nào khác không, hãy tìm kiếm lại trong database
        4. Giữ cho cuộc trò chuyện mang tính chất hỗ trợ và giúp đỡ.
        5. Khi nhận các câu hỏi không liên quan đến sản phẩm, hãy thân thiện hướng dẫn khách hàng đến các chủ đề liên quan đến các sản phẩm.
        6. Khi nhận các câu hỏi về thông tin sản phẩm, có thể lấy từ `Product Line Description` và `Product Description`, khi các câu hỏi liên quan đến thông số kỹ thuật, cấu hình như: màu sắc, dung lượng pin, camera, cấu hình, hãy sử dụng `Specs` để trả lời.
        7. Khi được hỏi link hoặc url của sản phẩm. hãy lấy thông tin từ `Url` và đính kèm format: `Links: {url}`
        8. Khi được hỏi về giá sản phẩm, hãy lấy thông tin từ `Prhình
        Hãy làm cho khách hàng cảm thấy được chào đón và quan tâm!
        """
        system_prompt = [{"role": "system", "content": system_prompt_content}]
        session_msgs = self.__construct_session_messages__(session_id)
        user_prompt = [{"role": "user", "content": enhanced_message}]
        messages = system_prompt + session_msgs + user_prompt

        try:
            response_text = llm.chat(messages)
        except:
            response_text = gemini_llm.chat(messages)

        # Lưu history
        self.__record_human_prompt__(session_id, enhanced_message, original_message)
        self.__record_ai_response__(session_id, response_text)

        # Cache nếu cần
        if cache_response and query_embedding:
            self.__cache_ai_response__(enhanced_message, original_message, response_text, query_embedding)

        return response_text

    def __construct_session_messages__(self, session_id: str):
        session_messages = self.history_collection.get(where_document={"$contains": session_id})
        result = []
        if not session_messages.get('ids'):
            return result
        for doc in session_messages.get('documents', []):
            hist = json.loads(doc).get('History', {})
            role = OPEN_AI_ROLE_MAPPING.get(hist.get('type', 'human'), 'user')
            content = hist.get('data', {}).get('content', '')
            result.append({"role": role, "content": content})
        return result

    def __record_human_prompt__(self, session_id: str, enhanced_message: str, original_message: str):
        self.history_collection.add(
            ids=[str(uuid.uuid4())],
            documents=[json.dumps({
                "SessionId": session_id,
                "History": {
                    "type": "human",
                    "data": {
                        "type": "human",
                        "content": original_message,
                        "enhanced_content": enhanced_message
                    }
                }
            })]
        )

    def __record_ai_response__(self, session_id: str, response_text: str):
        self.history_collection.add(
            ids=[str(uuid.uuid4())],
            documents=[json.dumps({
                "SessionId": session_id,
                "History": {
                    "type": "ai",
                    "data": {"type": "ai", "content": response_text}
                }
            })]
        )

    def __cache_ai_response__(self, enhanced_message: str, original_message: str, response_text: str, query_embedding: list):
        self.semantic_cache_collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[query_embedding],
            documents=[json.dumps({
                "text": [{"type": "human", "content": original_message, "enhanced_content": enhanced_message}],
                "llm_string": {"model_name": "gpt-4o-mini", "name": "ChatOpenAI"},
                "return_val": [{"type": "ai", "content": response_text}]
            })]
        )


class GuardedRAGAgent:
    """
    Agent RAG multi-turn với query rewriting / summarization.
    - Dùng chatHistory để tạo câu hỏi standalone.
    - Tìm document RAG dựa trên rewritten query.
    - Fallback Reflection nếu không tìm đủ document.
    """
    def __init__(
        self,
        rag: RAG,
        embedding_client: OpenAI,
        embedding_model: str,
        fallback_reflection: Reflection = None,
        similarity_threshold: float = 0.75,
        max_last_items: int = 100
    ):
        self.rag = rag
        self.embedding_client = embedding_client
        self.embedding_model = embedding_model
        self.fallback_reflection = fallback_reflection
        self.similarity_threshold = similarity_threshold
        self.max_last_items = max_last_items
        self.last_rewritten_query = ""

    def is_product_query(self, query: str, tags: list[str]) -> bool:
        """Check sơ bộ query có liên quan sản phẩm."""
        prompt = f"""
            Given the user query: {query}
            And the following product tags: {tags}
            Is this query related to a product? Respond with "yes" or "no".
        """
        response = self.fallback_reflection.raw_chat([{"role": "human", "content": prompt}])
        log.debug(f"[DEBUG] Product query check response: {response}")
        return response.lower() == "yes"

    def __rewrite_query(self, chat_history, query):
        """Tạo câu hỏi standalone dựa trên chat history dài hạn."""
        history_to_use = chat_history[-self.max_last_items:] if len(chat_history) > self.max_last_items else chat_history
        historyString = "\n".join([f"{h['role']}: {h['content']}" for h in history_to_use])

        prompt = [{
            "role": "user",
            "content": f"""
                Given a chat history and the latest user question, formulate a standalone question in Vietnamese which can be understood without the chat history. 
                Chat history:
                {historyString}
                User question: {query}
                Do NOT answer, just rewrite or return the question as-is.
            """
        }]

        rewritten = self.fallback_reflection.raw_chat(prompt)
        log.debug(f"[DEBUG] Rewritten query: {rewritten[:300]}")  # show first 300 chars
        self.last_rewritten_query = rewritten
        return rewritten

    def invoke(self, query: str, tags: list[str] = [], session_id: str = ""):
        log.debug(f"[DEBUG] Incoming query: {query}")

        # 1. Nếu query không liên quan sản phẩm
        if not self.is_product_query(query, tags):
            print("[DEBUG] Query không liên quan sản phẩm.")
            if self.fallback_reflection:
                output = self.fallback_reflection.chat(
                    session_id=session_id,
                    enhanced_message=query,
                    original_message=query,
                    cache_response=False
                )
                print(f"[DEBUG] Fallback Reflection output: {output[:200]}...")
                return {"output": output}
            return {"output": "Không tìm thấy dữ liệu"}

        # 2. Lấy toàn bộ chatHistory
        chatHistory = self.fallback_reflection.__construct_session_messages__(session_id) if self.fallback_reflection else []

        # 3. Rewrite query thành standalone
        rewritten_query = self.__rewrite_query(chatHistory, query)

        # 4. Tạo embedding cho rewritten query
        query_embedding = self.embedding_client.embeddings.create(
            model=self.embedding_model,
            input=rewritten_query
        ).data[0].embedding

        # 5. Lấy document từ RAG
        results = self.rag.hybrid_search(query_embedding, limit=5)
        log.debug(f"[DEBUG] Retrieved {len(results)} documents from RAG")
        for r in results:
            log.debug(f"  _id={r['_id']}, title={r['title']}, distance={r['distance']:.4f}")

        # 6. Filter theo similarity threshold
        filtered_results = [r for r in results if r['distance'] >= self.similarity_threshold]
        log.debug(f"[DEBUG] Filtered {len(filtered_results)} docs with similarity >= {self.similarity_threshold}")
        for r in filtered_results:
            log.debug(f"  _id={r['_id']}, title={r['title']}, distance={r['distance']:.4f}")

        if not filtered_results:
            log.debug("[DEBUG] Không có document đủ similarity, fallback Reflection.")
            if self.fallback_reflection:
                output = self.fallback_reflection.chat(
                    session_id=session_id,
                    enhanced_message=query,
                    original_message=query,
                    cache_response=False
                )
                log.debug(f"[DEBUG] Fallback Reflection output: {output[:200]}...")
                return {"output": output}
            return {"output": "Không tìm thấy dữ liệu"}

        # 7. Ghép prompt từ các document
        prompt_docs = "\n".join([
            f"Title: {r['title']}, Content: {r['description']}, Price: {r['price']}, Brand: {r['brand']}"
            for r in filtered_results
        ])

        # 8. Tạo message list cho LLM (multi-turn)
        messages = [{"role": "system", "content": "Bạn là chatbot cửa hàng bán đồ công nghệ hi-tech, thân thiện."}]
        messages += chatHistory[-self.max_last_items:]  # giữ multi-turn context
        messages.append({"role": "system", "content": f"Thông tin sản phẩm liên quan:\n{prompt_docs}"})
        messages.append({"role": "user", "content": query})

        # 9. Gọi LLM
        llm = OpenAiClient()
        response = llm.chat(messages)
        log.debug(f"[DEBUG] LLM output (first 300 chars): {response[:300]}")

        # 10. Lưu history
        if self.fallback_reflection:
            self.fallback_reflection.__record_human_prompt__(session_id, query, query)
            self.fallback_reflection.__record_ai_response__(session_id, response)

        return {"output": response}
