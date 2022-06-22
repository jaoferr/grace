from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.services.auth import AuthService
from app.routers.api_v1.config import Config

router = APIRouter(
    prefix=Config.PREFIX + '/auth',
    tags=[Config.TAG, 'auth'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.login', response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends()
):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise auth_service.settings.Exceptions.UNAUTHORIZED
    
    access_token_expires = timedelta(minutes=auth_service.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await auth_service.create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('.me', response_model=schemas.UserOut, response_model_by_alias=False)
async def get_me(auth_service: AuthService = Depends()):
    return await auth_service.get_current_user()
