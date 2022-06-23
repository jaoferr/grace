from fastapi import APIRouter, HTTPException
from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import User
from app.routers.api_v1.config import Config
from app.services.user import UserService
from app.utils.service_result import handle_result

router = APIRouter(
    prefix=Config.PREFIX + '/users',
    tags=[Config.TAG, 'users'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.get_by_id', response_model=schemas.UserOut, response_model_by_alias=False)
async def get_by_id(user_id: PydanticObjectId):
    result = await UserService().get_user(id=user_id)
    return handle_result(result)

@router.post('.create', response_model=schemas.UserOut, response_model_by_alias=False)
async def create(user: schemas.UserCreate):
    result = await UserService().create_user(user)
    return handle_result(result)
