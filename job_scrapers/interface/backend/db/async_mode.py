from typing import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.orm import Session, sessionmaker

from ..config import APISettings, get_api_settings

config: APISettings = get_api_settings()

DATABASE_URL_ASYNC: str = config.SQLALCHEMY_DATABASE_URI.replace(
    "sqlite", "sqlite+aiosqlite"
)


engine: AsyncEngine = create_async_engine(
    DATABASE_URL_ASYNC,
    connect_args=config.SQLALCHEMY_DATABASE_CONNECT_DICT,
    future=True,
    echo=False,
)

# async_session: sessionmaker = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession,
# )

async_session = async_sessionmaker(engine, expire_on_commit=False)

# Dependency
async def get_ses() -> AsyncGenerator[Session, None]:
    async with async_session.begin() as ses:
        yield ses


# async with async_session() as session:
#     query = await session.execute(select(A).where(A.name == name))
#     result = query.scalar()
#     result = query.scalar()

