from typing import AsyncIterator, Type

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.configs.database import DATABASE_URL
from src.configs.environment import get_environment_variables


env = get_environment_variables()

engine = create_async_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

session_local = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


async def init_database(base: Type[DeclarativeBase]):  # Passing class here
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with session_local() as session:
        yield session
