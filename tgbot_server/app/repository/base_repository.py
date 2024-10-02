from typing import TypeVar, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DuplicatedError
from app.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(self, async_session: AsyncSession, model: Type[T]) -> None:
        self.session = async_session
        self.model = model

    async def create(self, schema: T) -> int:
        query = self.model(**schema.model_dump())
        try:
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
        except IntegrityError as e:
            raise DuplicatedError(detail=str(e.orig))
        return query.id

    async def read_by_id(self, id: int) -> T | None:
        result = await self.session.get(self.model, id)
        if result:
            return T.from_orm(result)
        return result
