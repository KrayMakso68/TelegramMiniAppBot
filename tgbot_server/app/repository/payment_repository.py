from sqlalchemy import select, Result
from sqlalchemy.exc import DatabaseError, IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DBError, DuplicatedError
from app.model import Payment
from app.model.payment_model import PaymentOptions
from app.repository.interfaces import IPaymentRepository
from app.schema.payment_schema import PaymentCreate, PaymentSchema, PaymentUpdate, PaymentOptionSchema


class PaymentRepository(IPaymentRepository):
    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    async def add(self, payment_create: PaymentCreate) -> PaymentSchema:
        query: Payment = Payment(**payment_create.model_dump())
        try:
            self.session.add(query)
            await self.session.commit()
            await self.session.refresh(query)
        except IntegrityError as e:
            raise DuplicatedError(detail=str(e.orig))
        except DatabaseError:
            raise DBError(detail="Database error occurred.")
        return PaymentSchema.model_validate(query)

    async def get_by_id(self, id: int) -> PaymentSchema | None:
        try:
            result: Payment | None = await self.session.get(Payment, id)
            if result:
                return PaymentSchema.model_validate(result)
            return None
        except DatabaseError:
            raise DBError(detail="Database error occurred.")

    async def update(self, payment_id: int, payment_update: PaymentUpdate) -> PaymentSchema | None:
        try:
            stmt = select(Payment).where(Payment.id.c == payment_id)
            result: Result = await self.session.execute(stmt)
            payment = result.scalar_one()

            update_data = payment_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(payment, field, value)

            await self.session.commit()
            await self.session.refresh(payment)

            return payment
        except NoResultFound:
            return None

    async def get_all(self, user_id: int) -> list[PaymentSchema]:
        try:
            stmt = select(Payment).where(Payment.user_id.c == user_id).order_by(Payment.created_at.desc())
            result: Result = await self.session.execute(stmt)
            payments_history = result.scalars().all()
            return [PaymentSchema.model_validate(payment) for payment in payments_history]
        except NoResultFound:
            return []

    async def get_options(self) -> list[PaymentOptionSchema]:
        try:
            result = await self.session.execute(
                select(PaymentOptions)
            )
            options = result.scalars().all()
            return [PaymentOptionSchema.model_validate(option) for option in options]
        except NoResultFound:
            return []
