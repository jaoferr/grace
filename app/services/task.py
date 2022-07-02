from beanie.odm.fields import PydanticObjectId

from app.services.main import GenericAppService
from app.utils.service_result import ServiceResult
from app.tasks.resume import ingest
from app.core.worker import celery


class TaskService(GenericAppService):
    
    async def ingest() -> ServiceResult:
        # talk to tika here?
        # add to db?
        # makes sense
        # not really, code is complex, should be split
        # just call engine then?
        # should engine talk to db?
        # engine -> crud?
        ingest.task.delay(3)
    
    async def process() -> ServiceResult:
        pass
    
    async def recommend() -> ServiceResult:
        pass
    
    async def get_task(self, *, id: PydanticObjectId) -> ServiceResult:
        pass
    
    async def test_worker(self, *, task_duration: int):
        pass
