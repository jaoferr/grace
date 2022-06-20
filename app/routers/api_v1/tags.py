from fastapi import APIRouter, Depends, HTTPException
from beanie.odm.fields import PydanticObjectId

from app import schemas
from app.models import User, Tag
from app.crud import tags as crud_tags
from app.auth.token import get_current_user
from app.routers.api_v1.config import Config


router = APIRouter(
    prefix=Config.PREFIX + '/tags',
    tags=[Config.TAG, 'tags'],
    responses={
        404: {'message': 'Not found'}
    }
)

@router.post('.create', response_model=schemas.TagOut, response_model_by_alias=False)
async def create(
    form_data: schemas.TagCreateExternal, 
    current_user: User = Depends(get_current_user),
):
    new_tag = schemas.TagCreate(
        user_id=current_user.id,
        name=form_data.name,
        description=form_data.description
    )
    
    create_result = await crud_tags.create_tag(new_tag)

    if isinstance(create_result, Tag):
        return create_result
    else:
        raise HTTPException(status_code=409, detail=create_result)

@router.get('.get_by_id', response_model=schemas.TagOut, response_model_by_alias=False)
async def get_by_id(tag_id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    if (tag := await crud_tags.get_by_id_and_user(tag_id=tag_id, user_id=current_user.id)) is None:
        raise HTTPException(404, 'tag not found')
    
    return tag

@router.get('.from_current_user', response_model=list[schemas.TagOut], response_model_by_alias=False)
async def get_from_current_user(
    skip: int = 0, limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    if not (jobs := await crud_tags.get_owned_by_user(current_user.id, skip, limit)):
        raise HTTPException(status_code=404, detail=f'user has no tags')
    return jobs
