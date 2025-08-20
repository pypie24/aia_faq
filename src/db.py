from typing import AsyncGenerator, Any

from redis.asyncio import Redis
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        # Create all tables in the database
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


async def get_redis() -> Redis:
    return Redis(host="redis", port=6379, db=0)


async def bulk_insert_ignore_conflicts(
        session: AsyncSession,
        model: Any,
        objects: list[dict],
        unique_fields: list[str]
) -> None:
    """Insert a list of objects into the database, ignoring conflicts."""
    stmt = insert(model).values([obj for obj in objects])
    stmt = stmt.on_conflict_do_nothing(index_elements=unique_fields)
    await session.execute(stmt)
    await session.commit()
