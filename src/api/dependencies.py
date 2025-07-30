from fastapi.params import Depends

from src.services.knowleadge_services import KnowledgeService
from src.db import get_db


def get_knowledge_service(db=Depends(get_db)):
    return KnowledgeService(db)
