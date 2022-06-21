from fastapi import APIRouter, Depends, HTTPException

from app.models import User, Job
from app import schemas
from app.services.auth.token import get_current_user
from app.crud import jobs as crud_jobs
from app.routers.api_v1.config import Config

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
):
    if not (jobs := await crud_jobs.get_owned_by_user(current_user.id, skip, limit)):
        raise HTTPException(status_code=404, detail=f'user has no jobs')
    return jobs

@router.post('.create', response_model=schemas.JobOut, response_model_by_alias=False)
async def create(
    new_job: schemas.JobCreateExternal, 
    current_user: User = Depends(get_current_user)
):
    create_result = await crud_jobs.create_job(
        schemas.JobCreate(user_id=current_user.id, **new_job.dict())
    )

    if isinstance(create_result, Job):
        return create_result
    else:
        raise HTTPException(status_code=409, detail=create_result)

from beanie import PydanticObjectId
@router.get('.get_by_id', response_model=schemas.JobOut, response_model_by_alias=False)
async def get_by_id(
    job_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    if not (job := await crud_jobs.get_by_id_and_user(job_id, current_user.id)):
        raise HTTPException(status_code=404, detail=f'job not found')
    return job
