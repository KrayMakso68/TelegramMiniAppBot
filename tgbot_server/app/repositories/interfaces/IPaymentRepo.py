from abc import ABC, abstractmethod

from app.schema.payment_schema import PaymentCreate, PaymentSchema, PaymentUpdate, PaymentOptionSchema


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
