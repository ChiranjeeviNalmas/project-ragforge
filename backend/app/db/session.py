# provides the shared async database engine used across the app

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_database_url

engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global engine
    if engine is None:
        engine = create_async_engine(get_database_url(), echo=False)
    return engine
