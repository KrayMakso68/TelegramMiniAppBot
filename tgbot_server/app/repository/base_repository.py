from typing import TypeVar, AsyncGenerator, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(self, async_session: AsyncGenerator[AsyncSession, None], model: Type[T]) -> None:
        self.async_session = async_session
        self.model = model

    async def create(self, schema: T):