from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, DatabaseError

from app.repository.interfaces import IUserRepository
from app.core.exceptions import NotFoundError, DuplicatedError, DBError
from app.model.user_model import User
from app.schema.user_schema import UserCreate, UserSchema


class UserRepository(IUserRepository):
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def add(self, user_create: UserCreate) -> UserSchema:
        query: User = User(**user_create.model_dump())
        try:
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
        except IntegrityError as e:
            raise DuplicatedError(detail=str(e.orig))
        except DatabaseError:
            raise DBError(detail="Database error occurred.")
        return UserSchema.model_validate(query)

    async def get_by_id(self, id: int) -> UserSchema | None:
        try:
            result: User | None = await self.session.get(User, id)
            if result:
                return UserSchema.model_validate(result)
            return None
        except DatabaseError:
            raise DBError(detail="Database error occurred.")

    async def get_by_tg_id(self, tg_id: int) -> UserSchema | None:
        try:
            stmt = select(User).where(User.tg_id == tg_id)
            result: Result = await self.session.execute(stmt)
            user: User | None = result.scalar_one_or_none()
            if user:
                return UserSchema.model_validate(user)
            return None
        except DatabaseError:
            raise DBError(detail="Database error occurred.")
