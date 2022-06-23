from beanie.odm.fields import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from app.schemas import TagCreate, TagCreateExternal
from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException
from app.crud import tag as crud_tag



class TagService(GenericAppService):
    async def create_tag(
        self,
        new_tag: TagCreateExternal,
        user_id: PydanticObjectId
    ) -> ServiceResult:
        tag_in_db = TagCreate(
            user_id=user_id,
            name=new_tag.name,
            description=new_tag.description
        )
        try:
            tag = await crud_tag.create_tag(tag_in_db)
        except DuplicateKeyError:
            context = {'detail': 'tag already exists'}
            return ServiceResult(AppException.DuplicateEntryException(context))
    
        return ServiceResult(tag)
    
    async def get_tag(
        self,
        *,
        id: PydanticObjectId = None,
        name: str = None,
        user_id: PydanticObjectId = None
    ) -> ServiceResult:
        if id:
            tag = await crud_tag.get_by_id_and_user(user_id=user_id, id=id)
        elif name:
            tag = await crud_tag.get_by_user_and_name(user_id=user_id, name=name)
        
        if not tag:
            context = {'detail': 'tag not found'}
            return ServiceResult(AppException.EntryNotFound(context))
        
        return ServiceResult(tag)

    async def get_tag_multi(
        self,
        *,
        user_id: PydanticObjectId = None,
        skip: int = 0,
        limit: int = 20
    ) -> ServiceResult:
        if user_id:
            tags = await crud_tag.get_owned_by_user(
                user_id=user_id,
                skip=skip,
                limit=limit
            )
        
        if not tags:
            context = {'detail': 'user has no tags'}
            return ServiceResult(AppException.EntryNotFound(context))
        
        return ServiceResult(tags)
