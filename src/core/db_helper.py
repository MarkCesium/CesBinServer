from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from src.core.config import settings


class DataBaseHelper:
    def __init__(self, async_url: str, sync_url: str, echo: bool) -> None:
        self.async_engine = create_async_engine(
            url=async_url,
            echo=echo,
        )
        self.sync_engine = create_engine(
            url=sync_url,
            echo=echo,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.sync_session_factory = sessionmaker(
            bind=self.sync_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def async_session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session


db_helper = DataBaseHelper(str(settings.database.url), str(settings.database.sync_url), settings.database.echo)
