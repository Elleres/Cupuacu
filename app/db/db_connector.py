import os

from contextlib import asynccontextmanager

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# Looks up in the .env file for a DATABASE_URL variable; the second string is the default value in case the variable is
# not found
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost/db")

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
        async with self.async_session() as session:
            yield session

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = DatabaseConnector(DATABASE_URL)
