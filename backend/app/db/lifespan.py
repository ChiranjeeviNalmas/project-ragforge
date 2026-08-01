# runs startup checks and table creation around the app's request-serving lifetime

from contextlib import asynccontextmanager

from app.db.create_tables import create_all_tables
from app.db.health_check import check_database_connection
from app.db.session import get_engine


@asynccontextmanager
async def lifespan(app):
    await check_database_connection()
    await create_all_tables()
    try:
        yield
    finally:
        await get_engine().dispose()
