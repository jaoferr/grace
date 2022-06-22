from datetime import datetime, timedelta
from typing import Optional
from base64 import b64encode
from secrets import token_bytes

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseSettings

from app import schemas
from app.routers.api_v1.config import Config
from app.services.main import GenericAppService


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


default_auth_settings = AuthSettings()
default_pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
default_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Config.PREFIX + '/auth.login')

class AuthService(GenericAppService):

    def __init__(
        self,
        pwd_context = default_pwd_context,
        oauth2_scheme = default_oauth2_scheme,
        auth_settings = default_auth_settings
    ):
        self.pwd_context = pwd_context
        self.oauth2_scheme = oauth2_scheme
        self.settings = auth_settings

    async def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def authenticate_user(self, username: str, password: str):
        from app.crud import user as crud_users  # TEMP
        if not (user := await crud_users.get_by_username(username)):
            return False
        if not await self.verify_password(password, user.password):
            return False
        return user

    async def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)
        return encoded_jwt

    async def get_current_user(self) -> schemas.UserOut:
        token: str = self.oauth2_scheme
        try:
            payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
            username: str = payload.get('sub')
            if username is None:
                raise self.settings.Exceptions.CREDENTIALS
            token_data = schemas.TokenData(username=username)
        except JWTError:
            raise self.settings.Exceptions.CREDENTIALS
        user = await crud_users.get_by_username(username=token_data.username)
        if user is None:
            raise self.settings.Exceptions.CREDENTIALS
        return user
