from app.repository.interfaces import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
