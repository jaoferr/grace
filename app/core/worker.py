from celery import Celery
from celery.utils.log import get_task_logger

from app.core.config import settings


def get_celery():
    _celery = Celery(__name__)
    _celery.conf.broker_url = settings.assemble_celery_broker_url()
    _celery.conf.result_backend = settings.assemble_celery_broker_url()
    _celery.autodiscover_tasks([
        'app.tasks.resume'
    ])

    return _celery

def update_progress(self, current: int, total: int):
    progress = round((current + 1) / total * 100, 2)
    self.update_state(
        state='PROGRESS',
        meta={'progress': progress}
    )
    
celery = get_celery()
celery_logger = get_task_logger(__name__)