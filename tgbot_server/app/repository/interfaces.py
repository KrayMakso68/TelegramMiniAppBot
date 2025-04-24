from abc import ABC, abstractmethod

from app.schema.connect_schema import ConnectSchema
from app.schema.payment_schema import PaymentCreate, PaymentSchema, PaymentUpdate, PaymentOptionSchema
from app.schema.server_schema import ServerSchema, ServerInfo
from app.schema.subscription_schema import SubscriptionCreate, SubscriptionSchema
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

    @abstractmethod
    async def get_user_balance(self, id: int) -> float | None:
        raise NotImplementedError

    @abstractmethod
    async def update_balance(self, id: int, amount: float) -> UserSchema | None:
        raise NotImplementedError


class IPaymentRepository(ABC):
    @abstractmethod
    async def add(self, payment_create: PaymentCreate) -> PaymentSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> PaymentSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, user_id: int) -> list[PaymentSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, payment_id: int, payment_update: PaymentUpdate) -> PaymentSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_options(self) -> list[PaymentOptionSchema]:
        raise NotImplementedError


class ISubscriptionRepository(ABC):
    @abstractmethod
    async def add(self, subscription_create: SubscriptionCreate) -> SubscriptionSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> SubscriptionSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_grouped(self, user_id: int) -> dict[str, list[SubscriptionSchema]]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_from_server(self, user_id: int, server_id: int) -> list[SubscriptionSchema]:
        raise NotImplementedError

    @abstractmethod
    async def update_subscription_by_connect(self, sub_id: int, connect: ConnectSchema) -> SubscriptionSchema:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, sub_id: int) -> bool:
        raise NotImplementedError


class IServerRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[ServerSchema]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> ServerSchema | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_short_info(self) -> list[ServerInfo]:
        raise NotImplementedError
