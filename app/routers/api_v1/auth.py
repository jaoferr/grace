from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.services.auth.config import auth_settings
from app.services.auth.token import (
    Token,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.routers.api_v1.config import Config

router = APIRouter(
    prefix=Config.PREFIX + '/auth',
    tags=[Config.TAG, 'auth'],
    responses={
        404: {'message': 'Not found'}
    }
)


@router.post('.login', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise auth_settings.Exceptions.UNAUTHORIZED
    
    access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
    
@router.get('.me', response_model=schemas.UserOut, response_model_by_alias=False)
def get_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user
