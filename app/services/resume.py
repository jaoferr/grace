from typing import BinaryIO

from beanie.odm.fields import PydanticObjectId
from fastapi import Depends

from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException
from app.utils.file_handling import validate_file_size, validate_content_type
from app.tasks.resume.tasks import ingest
from app.engines.ingesting.engine import IngestingEngine
from app.schemas import TaskOut

class ResumeService(GenericAppService):
 
    async def create_resumes(
        self,
        *,
        file: BinaryIO,
        content_type: str,
        user_id: PydanticObjectId,
        ingesting_engine: IngestingEngine = Depends()
    ) -> ServiceResult:
        if not await validate_file_size(file):
            return ServiceResult(AppException.FileTooLarge())
        
        if not await validate_content_type(content_type):
            context = {'detail': f'content {content_type} is not allowed'}
            return ServiceResult(AppException.InvalidFileType(context=context))
 
        task_result = ingest.delay(task_duration=3)
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

