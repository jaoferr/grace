from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId

from app import schemas
from app.models import User, Job
from app.services.auth import get_current_user
from app.crud import job as crud_jobs
from app.routers.api_v1.config import Config
from app.services.job import JobService
from app.utils.service_result import handle_result

router = APIRouter(
    prefix=Config.PREFIX + '/jobs',
    tags=[Config.TAG, 'jobs'],
    responses={
        404: {'message': 'Not found'}
    },
    
)

@router.get('.from_current_user', response_model=list[schemas.JobOut], response_model_by_alias=False)
async def get_from_current_user(
    skip: int = 0, limit: int = 20,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends()
):
    current_user = handle_result(current_user)
    result = await job_service.get_job_multi(
        user_id=current_user.id,
        skip=skip, limit=limit
    )
    return handle_result(result)
    

@router.post('.create', response_model=schemas.JobOut, response_model_by_alias=False)
async def create(
    new_job: schemas.JobCreateExternal, 
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends()
):
    current_user = handle_result(current_user)
    result = await job_service.create_job(
        new_job=new_job,
        user_id=current_user.id
    )
    return handle_result(result)

@router.get('.get_by_id', response_model=schemas.JobOut, response_model_by_alias=False)
async def get_by_id(
    job_id: PydanticObjectId,
    current_user: User = Depends(get_current_user),
    job_service: JobService = Depends()
):
    current_user = handle_result(current_user)
    result = await job_service.get_job(
        id=job_id,
        user_id=current_user.id
    )
    return handle_result(result)
