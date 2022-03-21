from pydantic import BaseSettings
from secrets import token_bytes
from base64 import b64encode
from fastapi import HTTPException

class AuthSettings(BaseSettings):

    SECRET_KEY: str = b64encode(token_bytes(32)).decode()
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Exceptions:
        CREDENTIALS = HTTPException(
            401, detail='could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        DISABLED = HTTPException(
            400, detail='user is disabled'
        )
        UNAUTHORIZED = HTTPException(
            401, detail='incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

auth_settings = AuthSettings()
