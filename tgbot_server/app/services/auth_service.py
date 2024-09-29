from app.repository.user_repository import UserRepository
from app.schema.auth_schema import WebAppInitData
from app.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    def login(self, login_info: WebAppInitData):
        ...
