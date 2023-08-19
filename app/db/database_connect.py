from typing import AsyncGenerator
from aioredis import ConnectionPool, Redis

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    REDIS_URL
)

# Формируем URL для подключения
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создаем асинхронную сессию
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

async_session_maker = sessionmaker(class_=AsyncSession,
                                   expire_on_commit=False,
                                   bind=engine,
                                   autoflush=False,
                                   autocommit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает сессию соединения с базой данных"""
    async with async_session_maker() as async_session:
        yield async_session


def create_redis():
    """Создание пула соединений с Redis"""
    return ConnectionPool.from_url(REDIS_URL)


redis_connection_pool = create_redis()


def get_redis():
    """Получение соединения с Redis"""
    return Redis(connection_pool=redis_connection_pool)
