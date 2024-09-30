from typing import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.repository.base_repository import BaseRepository
from app.model.user import User


class UserRepository(BaseRepository):
    def __init__(self, async_session: Callable[..., AsyncGenerator[AsyncSession, None]] = get_async_session):
        self.async_session = async_session
        super().__init__(async_session, User)
