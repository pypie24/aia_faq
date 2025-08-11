from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import init_db
from src.config import settings
from src.api.v1.brand_api import router as brands_router_v1
from src.api.v1.category_api import router as categories_router_v1
from src.api.v1.product_api import router as products_router_v1
from src.api.v1.image_api import router as images_router_v1
from src.api.v1.tag_api import router as tags_router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=settings.TITLE,
        version=settings.VERSION,
        debug=settings.DEBUG,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(brands_router_v1, prefix="/api/v1")
    app.include_router(categories_router_v1, prefix="/api/v1")
    app.include_router(products_router_v1, prefix="/api/v1")
    app.include_router(images_router_v1, prefix="/api/v1")
    app.include_router(tags_router_v1, prefix="/api/v1")
    return app


app = create_app()
