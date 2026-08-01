# loads runtime database settings from the environment

import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
    )
