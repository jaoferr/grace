from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.services.auth import login_user, get_current_user
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
    access_token = await login_user(
        username=form_data.username,
        password=form_data.password
    )
    return handle_result(access_token)

@router.get('.me', response_model=schemas.UserOut, response_model_by_alias=False)
async def get_me(current_user: User = Depends(get_current_user)):
    return handle_result(current_user)
