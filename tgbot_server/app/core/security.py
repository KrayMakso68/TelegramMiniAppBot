from datetime import timedelta, datetime, timezone

import jwt
from fastapi.security import OAuth2PasswordBearer
from app.core.config import configs

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, configs.JWT_SECRET_KEY, algorithm=configs.ALGORITHM)
    return encoded_jwt
