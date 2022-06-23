from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult
from app.utils.app_exceptions import AppException


class ResumeService(GenericAppService):
    async def create_resume() -> ServiceResult:
        pass
    
    async def get_resume() -> ServiceResult:
        pass
    
    async def delete_resume() -> ServiceResult:
        pass
    
    async def start_task() -> ServiceResult:
        pass
