# creates all sqlalchemy model tables against the database on startup

from app.db.base import Base
from app.db.session import get_engine
from app.models.tenant import Tenant  # noqa: F401


async def create_all_tables() -> None:
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
