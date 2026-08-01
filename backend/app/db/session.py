# manages the async database engine and startup verification

from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_database_url

engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global engine
    if engine is None:
        engine = create_async_engine(get_database_url(), echo=False)
    return engine


async def check_database_connection() -> None:
    conn = await get_engine().connect()
    try:
        await conn.execute(text("SELECT 1"))
        result = await conn.execute(text("SELECT extname FROM pg_extension WHERE extname='vector'"))
        if result.scalar() is None:
            raise RuntimeError("pgvector extension is not available")
    finally:
        await conn.close()


@asynccontextmanager
async def lifespan(app):
    await check_database_connection()
    try:
        yield
    finally:
        await get_engine().dispose()
