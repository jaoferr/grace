from beanie.odm.fields import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from app.services.main import GenericAppService
from app.schemas import JobCreate, JobCreateExternal
from app.utils.service_result import ServiceResult
from app.crud import job as crud_job
from app.utils.app_exceptions import AppException


class JobService(GenericAppService):
    async def create_job(
        self,
        new_job: JobCreateExternal,
        user_id: PydanticObjectId
    ) -> ServiceResult:
        job_in_db = JobCreate(
            name=new_job.name,
            description=new_job.description,
            user_id=user_id
        )
        try:
            job = await crud_job.create_job(job_in_db)
        except DuplicateKeyError:
            context = {'detail': 'job already exists'}
            return ServiceResult(AppException.DuplicateEntryException(context))
        
        return ServiceResult(job)
    
    async def get_job(
        self,
        *,
        user_id: PydanticObjectId,
        id: PydanticObjectId = None,
        name: str = None
    ) -> ServiceResult:
        if id:
            job = await crud_job.get_by_id_and_user(user_id=id, id=id)
        elif name:
            job = await crud_job.get_by_user_and_name(user_id=user_id, name=name)
            
        if not job:
            context = {'detail': 'job not found'}
            return ServiceResult(AppException.EntryNotFound(context))

        return ServiceResult(job)
    
    async def get_job_multi(
        self,
        *,
        user_id: PydanticObjectId = None,
        skip: int = 0,
        limit: int = 20
    ) -> ServiceResult:
        if user_id:
            jobs = await crud_job.get_owned_by_user(user_id, skip, limit)
        
        if not jobs:
            context = {'detail': 'user has no jobs'}
            return ServiceResult(AppException.EntryNotFound(context))
        
        return ServiceResult(jobs)
