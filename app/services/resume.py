from typing import BinaryIO

from beanie.odm.fields import PydanticObjectId
from fastapi import Depends

from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException
from app.utils.file_handling import validate_file_size, validate_content_type
from app.tasks.resume.tasks import ingest
from app.schemas import TaskOut
from app.crud import temp_file_storage as crud_temp_file_storage

class ResumeService(GenericAppService):

    async def create_resumes(
        self,
        *,
        file: BinaryIO,
        content_type: str,
        user_id: PydanticObjectId,
        tag_id: PydanticObjectId
    ) -> ServiceResult:
        if not await validate_file_size(file):
            return ServiceResult(AppException.FileTooLarge())
        
        if not await validate_content_type(content_type):
            context = {'detail': f'content {content_type} is not allowed'}
            return ServiceResult(AppException.InvalidFileType(context=context))

        file.seek(0)
        temp_file_in_db = await crud_temp_file_storage.store(file.read())

        task_kwargs = {
            'temp_file_id': str(temp_file_in_db.id),
            'user_id': str(user_id),
            'tag_id': str(tag_id)
        }
        task_result = ingest.apply_async(
            kwargs=task_kwargs,
        )
        return ServiceResult(TaskOut(
            id=task_result.id,
            status=task_result.status
        ))

    async def generic_task(self, duration: int):
        task_result = ingest.delay(task_duration=duration)
        return ServiceResult(TaskOut(
            id=task_result.id,
            status=task_result.status
        ))
