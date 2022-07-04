from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.services.auth import (
    login_user,
    get_current_user,
    auth_settings
)
from app.routers.api_v1.config import Config
from app.models import User
from app.utils.service_result import handle_result

router = APIRouter(
    prefix=Config.PREFIX + '/auth',
    tags=[Config.TAG, 'auth'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.login', response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = await authenticate_user(form_data.username, form_data.password)
    # if not user.success:
    #     return handle_result(user)

    # access_token_expires = timedelta(minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = await create_access_token(
    #     data={'sub': user.username}, expires_delta=access_token_expires
    # )
    # return {'access_token': access_token, 'token_type': 'bearer'}
    access_token = await login_user(
        username=form_data.username,
        password=form_data.password
    )
    return handle_result(access_token)

@router.get('.me', response_model=schemas.UserOut, response_model_by_alias=False)
async def get_me(current_user: User = Depends(get_current_user)):
    return handle_result(current_user)
