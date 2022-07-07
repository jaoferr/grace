import time

from app.core.worker import celery, update_progress
from app.utils.service_result import ServiceResult
from app.schemas import TaskOut

@celery.task(name='generic', bind=True)
def generic(self, task_duration: int):
    for i in range(task_duration):
        progress = round((i + 1) / task_duration, 2) * 100
        print(f'Progress: {progress}%')
        time.sleep(1)
        
        update_progress(self, i, task_duration)

def generic_task(duration: int):
    task_result = generic.delay(task_duration=duration)
    return ServiceResult(TaskOut(
        id=task_result.id,
        status=task_result.status
    ))
