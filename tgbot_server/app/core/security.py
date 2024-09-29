from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    ...


def decode_token(token: str) -> dict:
    ...

