from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from src.db import engine
from src.api.knowledge_api import router as knowledge_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(lambda x: None)
    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(knowledge_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
