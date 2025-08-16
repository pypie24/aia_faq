from openai import OpenAI
from fastapi import APIRouter, WebSocket

from src.config import settings


llm = OpenAI(
    base_url=settings.OPENAI_ENDPOINT,
    api_key=settings.OPENAI_LLM_API_KEY
)


router = APIRouter()


@router.websocket("/chat/{user_id}")
async def chat_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = await llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": data}
            ]
        )
        await websocket.send_text(response.choices[0].message.content)
