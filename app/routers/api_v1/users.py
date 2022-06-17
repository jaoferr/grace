from fastapi import APIRouter, Depends, HTTPException

from app import schemas
from app.models import User
from app.crud import users as crud_users
from app.routers.api_v1.config import Config

router = APIRouter(
    prefix=Config.PREFIX + '/users',
    tags=[Config.TAG, 'users'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.get_by_id', response_model=schemas.UserOut)
async def get_user(user_id: int):
    if (user := await crud_users.get_by_id(user_id=user_id)) is None:
        raise HTTPException(404, 'User not found')
    return user

@router.post('.create', response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate):
    if (db_user := await crud_users.get_by_email(user.email)):
        raise HTTPException(status_code=400, detail='email already in use')
   
    new_user = await crud_users.create_user(user)
    return new_user
