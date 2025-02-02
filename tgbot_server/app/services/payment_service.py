from collections import defaultdict

from app.core.config import settings
from app.repository.interfaces import IPaymentRepository, IUserRepository
from app.schema.payment_schema import PaymentCreate, OperationType, PaymentStatus, PaymentUpdate, PaymentSchema, \
    YooMoneyData, PaymentOptionSchema
from app.utils import validate_yoomoney


class PaymentService:
    def __init__(
            self,
            payment_repository: IPaymentRepository,
            user_repository: IUserRepository
    ):
        self.payment_repository = payment_repository
        self.user_repository = user_repository

    async def new_yoomoney_payment(self, user_id: int, amount: float) -> str:
        create_payment = PaymentCreate(amount=amount,
                                       user_id=user_id,
                                       operation_type=OperationType.DEPOSIT
                                       )
        new_payment = await self.payment_repository.add(create_payment)
        quickpay_link = f"https://yoomoney.ru/quickpay/confirm.xml?receiver={settings.YOOMONEY_WALLET}&quickpay-form=button&paymentType=SB&sum={amount}&&label={new_payment.id}&successURL={settings.PAY_SUCCESS_URL}"
        return quickpay_link

    async def processing_yoomoney_payment(self, data: YooMoneyData) -> dict:
        if validate_yoomoney.verify_hash(data):
            payment_id = int(data.label)
            amount = float(data.withdraw_amount)
            payment = await self.payment_repository.update(payment_id, PaymentUpdate(status=PaymentStatus.COMPLETED))
            await self.user_repository.update_balance(payment.user_id, amount)

            return {"status": "OK"}
        else:
            return {"status": "Error"}

    async def get_group_payments_by_day(self, user_id: int) -> dict[str, list[PaymentSchema]]:
        payments = await self.payment_repository.get_all(user_id)
        grouped = defaultdict(list)
        for payment in payments:
            date = payment.created_at.date().strftime("%d.%m.%Y")
            grouped[date].append(payment)
        return grouped

    async def get_payment_options(self) -> list[PaymentOptionSchema]:
        return await self.payment_repository.get_options()
