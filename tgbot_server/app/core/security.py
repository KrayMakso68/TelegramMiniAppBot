import logging
from datetime import timedelta, datetime, timezone

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError, encode as encode_jwt, decode as decode_jwt

from app.core.config import configs
from app.core.exceptions import JwtCredentialsError
from app.schema.auth_schema import TokenData


async def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({"exp": int(expire.timestamp())})
    encoded_jwt = encode_jwt(payload, configs.JWT_SECRET_KEY, algorithm=configs.ALGORITHM)
    return encoded_jwt


async def decode_access_token(token: str) -> TokenData:
    try:
        payload = decode_jwt(token, configs.JWT_SECRET_KEY, algorithms=[configs.ALGORITHM])

        tg_id: int = payload.get("tg_id")
        if tg_id is None:
            raise JwtCredentialsError("Could not validate credentials", {"WWW-Authenticate": "Bearer"})

        exp = payload.get("exp")
        if exp is not None and exp < int(datetime.now(timezone.utc).timestamp()):
            raise JwtCredentialsError("Token has expired", {"WWW-Authenticate": "Bearer"})
        return TokenData(tg_id=tg_id)
    except InvalidTokenError:
        raise JwtCredentialsError("Could not validate credentials", {"WWW-Authenticate": "Bearer"})


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        try:
            decode_access_token(jwtoken)
            return True
        except JwtCredentialsError as e:
            logging.warning(f"JWT verification failed: {e.detail}")
            return False


oauth_scheme = JWTBearer()
