from fastapi import APIRouter, HTTPException
from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import User
from app.crud import user as crud_users
from app.routers.api_v1.config import Config

router = APIRouter(
    prefix=Config.PREFIX + '/users',
    tags=[Config.TAG, 'users'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.get_by_id', response_model=schemas.UserOut, response_model_by_alias=False)
async def get_by_id(user_id: PydanticObjectId):
    if (user := await crud_users.get_by_id(user_id=user_id)) is None:
        raise HTTPException(404, 'user not found')
    
    return user

@router.post('.create', response_model=schemas.UserOut, response_model_by_alias=False)
async def create(user: schemas.UserCreate):
    create_result = await crud_users.create_user(user)

    if isinstance(create_result, User):  # if create is successful, return newly created user
        return create_result
    else:  # else, return error message, defined in crud.create_user
        raise HTTPException(status_code=409, detail=create_result)
