import os

from contextlib import asynccontextmanager

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")  # default = development

if ENVIRONMENT == "dev":
    DATABASE_URL = os.getenv("DATABASE_URL")
elif ENVIRONMENT == "test":
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")
elif ENVIRONMENT == "production":
    DATABASE_URL = os.getenv("DATABASE_URL_PROD")
else:
    raise ValueError(f"ENVIRONMENT {ENVIRONMENT} não reconhecido!")

class DatabaseConnector:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self):
        async with self.async_session as session:
            yield session

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = DatabaseConnector(DATABASE_URL)

async def get_db():
    async with db.async_session() as session:
        yield session