from abc import ABC, abstractmethod

from app.schema.connect_schema import ConnectSchema
from app.schema.subscription_schema import SubscriptionCreate, SubscriptionSchema, SubscriptionUpdate


class ISubscriptionRepository(ABC):
    @abstractmethod
    async def add(self, subscription_create: SubscriptionCreate) -> SubscriptionSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> SubscriptionSchema | None:
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
    async def update(self, sub_id: int, update_info: SubscriptionUpdate):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, sub_id: int) -> bool:
        raise NotImplementedError
