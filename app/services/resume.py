from typing import BinaryIO

from beanie.odm.fields import PydanticObjectId

from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException
from app.utils.file_handling import validate_file_size, validate_content_type
from app.core.worker import add_task


class ResumeService(GenericAppService):
 
    async def process_file(
        self,
        *,
        file: BinaryIO,
        content_type: str,
        user_id: PydanticObjectId
    ) -> ServiceResult:
        if not await validate_file_size(file):
            return ServiceResult(AppException.FileTooLarge())
        
        if not await validate_content_type(content_type):
            context = {'detail': f'content {content_type} is not allowed'}
            return ServiceResult(AppException.InvalidFileType(context=context))
 
        task_result = await add_task(
            task=sum,
            file=file,
            number_2=20
        )

    async def get_resume() -> ServiceResult:
        pass
    
    async def delete_resume() -> ServiceResult:
        pass
    
    async def start_task() -> ServiceResult:
        pass

    async def validate_file() -> ServiceResult:
        pass
