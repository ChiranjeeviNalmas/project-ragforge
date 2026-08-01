# verifies the database is reachable and pgvector is enabled

from sqlalchemy import text

from app.db.session import get_engine


async def check_database_connection() -> None:
    conn = await get_engine().connect()
    try:
        await conn.execute(text("SELECT 1"))
        result = await conn.execute(text("SELECT extname FROM pg_extension WHERE extname='vector'"))
        if result.scalar() is None:
            raise RuntimeError("pgvector extension is not available")
    finally:
        await conn.close()
