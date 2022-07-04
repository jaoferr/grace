from datetime import datetime, timedelta
from typing import Optional
from base64 import b64encode
from secrets import token_bytes

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseSettings

from app import schemas
from app.routers.api_v1.config import Config
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException
from app.models import User


class AuthSettings(BaseSettings):

    SECRET_KEY: str = b64encode(token_bytes(32)).decode()
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

auth_settings = AuthSettings()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Config.PREFIX + '/auth.login')


async def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password: str):
    return pwd_context.hash(password)

from app.crud import user as crud_users

async def authenticate_user(username: str, password: str) -> bool:
    if not (user := await crud_users.get_by_username(username)):
        return False
    if await verify_password(password, user.password):
        return True
    return False

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    return encoded_jwt

async def login_user(username: str, password: str) -> ServiceResult:
    is_authenticated = await authenticate_user(username, password)
    if not is_authenticated:
        return ServiceResult(AppException.Unauthorized())
    
    encoded_jwt = await create_access_token(data={'sub': username})
    access_token = schemas.Token(
        access_token=encoded_jwt,
        token_type='bearer'
    )
    return ServiceResult(access_token)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> ServiceResult:
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            return ServiceResult(AppException.InvalidCredentials())
        token_data = schemas.TokenData(username=username)
    except JWTError:
        return ServiceResult(AppException.InvalidCredentials())
    user = await crud_users.get_by_username(username=token_data.username)
    if user is None:
        return ServiceResult(AppException.InvalidCredentials())
    return ServiceResult(user)
