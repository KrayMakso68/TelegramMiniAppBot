from typing import TypeVar, AsyncGenerator, Type, Callable

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DuplicatedError
from app.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(self, async_session: Callable[..., AsyncGenerator[AsyncSession, None]], model: Type[T]) -> None:
        self.async_session = async_session
        self.model = model

    async def create(self, schema: T) -> int:
        async with self.async_session() as session:
            query = self.model(**schema.dict())
            try:
                session.add(query)
                await session.commit()
                await session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return query.id
