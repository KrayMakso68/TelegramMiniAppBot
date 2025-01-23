from app.core.config import settings
from app.repository.interfaces import IPaymentRepository, IUserRepository
from app.schema.payment_schema import PaymentCreate, OperationType, PaymentStatus, PaymentUpdate, PaymentSchema


class PaymentService:
    def __init__(
            self,
            payment_repository: IPaymentRepository,
            user_repository: IUserRepository
    ):
        self.payment_repository = payment_repository
        self.user_repository = user_repository

    async def new_yoomoney_payment(self, user_id: int, amount: float) -> str:
        create_payment = PaymentCreate(amount=amount, user_id=user_id, operation_type=OperationType.DEPOSIT)
        new_payment = await self.payment_repository.add(create_payment)

        quickpay_link = f"https://yoomoney.ru/quickpay/confirm.xml?receiver={settings.YOOMONEY_WALLET}&quickpay-form=button&paymentType=SB&sum={amount}&&label={new_payment.id}&successURL={settings.PAY_SUCCESS_URL}"
        print(quickpay_link)

        return quickpay_link

    async def processing_payment(self, payment_id: int, amount: float) -> None:
        payment = await self.payment_repository.update(payment_id, PaymentUpdate(status=PaymentStatus.COMPLETED))
        await self.user_repository.update_balance(payment.user_id, amount)

    async def get_user_history(self, user_id: int) -> list[PaymentSchema]:
        return await self.payment_repository.get_all(user_id)
