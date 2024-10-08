from abc import ABC, abstractmethod

from app.schema.user_schema import UserCreate, UserSchema


class IUserRepository(ABC):
    @abstractmethod
    async def add(self, user_create: UserCreate) -> UserSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> UserSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> UserSchema | None:
        raise NotImplementedError
