from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.repository.base_repository import BaseRepository
from app.model.user_model import User
from app.schema.user_schema import User as UserSchema


class UserRepository(BaseRepository):
    def __init__(self, async_session: AsyncSession):
        self.session = async_session
        super().__init__(async_session, User)

    async def read_by_tg_id(self, tg_id: int) -> UserSchema | None:
        stmt = select(self.model).where(self.model.tg_id == tg_id)
        result: Result = await self.session.execute(stmt)
        user: User | None = result.scalar_one_or_none()
        if user:
            return UserSchema.from_orm(user)
        return user
