from fastapi import APIRouter, Depends, HTTPException
from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import User, Tag
from app.services.tag import TagService
from app.services.auth import get_current_user
from app.routers.api_v1.config import Config
from app.utils.service_result import handle_result


router = APIRouter(
    prefix=Config.PREFIX + '/tags',
    tags=[Config.TAG, 'tags'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.create', response_model=schemas.TagOut, response_model_by_alias=False)
async def create(
    new_tag: schemas.TagCreateExternal, 
    current_user: User = Depends(get_current_user),
    tag_service: TagService = Depends()
):
    current_user = handle_result(current_user)
    result = await tag_service.create_tag(
        new_tag=new_tag,
        user_id=current_user.id
    )
    return handle_result(result)

@router.get('.get_by_id', response_model=schemas.TagOut, response_model_by_alias=False)
async def get_by_id(
    tag_id: PydanticObjectId,
    current_user: User = Depends(get_current_user),
    tag_service: TagService = Depends()
):
    current_user = handle_result(current_user)
    result = await tag_service.get_tag(id=tag_id, user_id=current_user.id)
    return handle_result(result)

@router.get('.from_current_user', response_model=list[schemas.TagOut], response_model_by_alias=False)
async def get_from_current_user(
    skip: int = 0, limit: int = 20,
    current_user: User = Depends(get_current_user),
    tag_service: TagService = Depends()
):
    current_user = handle_result(current_user)
    result = await tag_service.get_tag_multi(
        user_id=current_user.id,
        skip=skip, limit=limit
    )
    return handle_result(result)
