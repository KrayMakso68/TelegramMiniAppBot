from typing import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import NotFoundError
from app.repository.base_repository import BaseRepository
from app.model.user import User


class UserRepository(BaseRepository):
    def __init__(self, async_session: Callable[..., AsyncGenerator[AsyncSession, None]] = get_async_session):
        self.async_session = async_session
        super().__init__(async_session, User)

    async def read_by_tg_id(self, tg_id: int) -> User | None:
        async with self.async_session() as session:
            query = session.query(self.model).filter(self.model.tg_id == tg_id).first()
            return query
