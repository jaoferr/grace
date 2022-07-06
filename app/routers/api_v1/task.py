from fastapi import APIRouter, Depends

from app.routers.api_v1.config import Config
from app.utils.service_result import handle_result
from app.schemas import TaskStatus


router = APIRouter(
    prefix=Config.PREFIX + '/tasks',
    tags=[Config.TAG, 'tasks'],
    responses={
        404: {'message': 'Not found'}
    }
)


from app.core.worker import celery
from app.utils.service_result import ServiceResult
from celery.result import AsyncResult
@router.get('.get')
def get_task_status(task_id: str) -> TaskStatus:
    task_result = AsyncResult(task_id, app=celery)
    if task_result.result:
        progress = task_result.result.get('progress')
    else:
        progress = False

    status = ServiceResult(TaskStatus(
        id=task_id,
        status=task_result.status,
        progress=progress
    ))
    return handle_result(status)

from app.services.resume import ResumeService
@router.post('.generic', response_model=None)
async def generic_task(
    duration: int,
    resume_service: ResumeService = Depends()
):

    result = await resume_service.generic_task(
        duration=duration
    )
    return handle_result(result)