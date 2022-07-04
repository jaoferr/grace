from typing import BinaryIO

from beanie.odm.fields import PydanticObjectId
from fastapi import Depends

from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException
from app.utils.file_handling import validate_file_size, validate_content_type
from app.tasks.resume import ingest
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
 
        task_result = await ingest.task(3, ingesting_engine)
        return ServiceResult(TaskOut(
            id=task_result.id,
            status='accepted'            
        ))


    async def get_resume() -> ServiceResult:
        pass
    
    async def delete_resume() -> ServiceResult:
        pass
    
    async def start_task() -> ServiceResult:
        pass

    async def validate_file() -> ServiceResult:
        pass
