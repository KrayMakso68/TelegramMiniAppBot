from app.core.config import settings


class PaymentService:
    def __init__(self, payment_repository: IPaymentRepository):
        self.payment_repository = payment_repository

    async def new_yoomoney_payment(self, user_id: int, amount: float) -> str:

        quickpay_link = f"https://yoomoney.ru/quickpay/confirm?receiver={settings.YOOMONEY_WALLET}&sum={amount}&label={user_id}&successURL={settings.PAY_SUCCESS_URL}"



        return quickpay_link
