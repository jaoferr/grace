from pymongo.errors import DuplicateKeyError
from beanie.odm.fields import PydanticObjectId

from app.services.main import GenericAppService
from app.schemas import UserCreate, UserCreateExternal
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException
from app.services.auth import get_password_hash
from app.crud import user as crud_user

class UserService(GenericAppService):
    async def create_user(self, new_user: UserCreateExternal) -> ServiceResult:
        user_in_db = UserCreate(
            username=new_user.username,
            email=new_user.email,
            password=await get_password_hash(new_user.password)
        )

        try:
            user = await crud_user.create_user(user_in_db)
        except DuplicateKeyError:
            context = {'detail': 'email already in use'}
            return ServiceResult(AppException.DuplicateEntryException(context))

        return ServiceResult(user)

    async def get_user(
        self,
        *, 
        id: PydanticObjectId = None,
        username: str = None,
        email: str = None
    ) -> ServiceResult:
        if id:
            user = await crud_user.get_by_id(id)
        elif username:
            user = await crud_user.get_by_username(username)
        elif email:
            user = await crud_user.get_by_email(email)
            
        if not user:
            return ServiceResult(AppException.EntryNotFound({'detail': 'user not found'}, is_public=True))

        return ServiceResult(user)