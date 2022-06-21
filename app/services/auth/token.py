from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app import schemas
from app.services.auth.config import auth_settings
from app.routers.api_v1.config import Config


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Config.PREFIX + '/auth.login')

async def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password: str):
    return pwd_context.hash(password)

from app.crud import user as crud_users

async def authenticate_user(username: str, password: str):
    if not (user := await crud_users.get_by_username(username)):
        return False
    if not await verify_password(password, user.password):
        return False
    return user

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.UserOut:
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise auth_settings.Exceptions.CREDENTIALS
        token_data = TokenData(username=username)
    except JWTError:
        raise auth_settings.Exceptions.CREDENTIALS
    user = await crud_users.get_by_username(username=token_data.username)
    if user is None:
        raise auth_settings.Exceptions.CREDENTIALS
    return user
