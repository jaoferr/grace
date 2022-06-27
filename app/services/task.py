from beanie.odm.fields import PydanticObjectId

from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult

class TaskService(GenericAppService):
    
    async def ingest() -> ServiceResult:
        pass
    
    async def process() -> ServiceResult:
        pass
    
    async def recommend() -> ServiceResult:
        pass
    
    async def get_task(self, *, id: PydanticObjectId) -> ServiceResult:
        pass
    