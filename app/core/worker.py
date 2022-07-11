from celery import Celery, Task
from celery.utils.log import get_task_logger

from app.core.config import settings

def get_celery():
    _celery = Celery(__name__)
    _celery.conf.broker_url = settings.assemble_celery_broker_url()
    _celery.conf.result_backend = settings.assemble_celery_broker_url()
    _celery.autodiscover_tasks([
        'app.tasks.resume',
        'app.tasks.generic'
    ])

    return _celery

def update_progress(self: Task, current: int, total: int):
    progress = round((current + 1) / total * 100, 2)
    self.update_state(
        state='PROGRESS',
        meta={'progress': progress}
    )

# from celery.signals import celeryd_init
# from asyncio import get_event_loop
# from app.core.database import get_motor_client, init_db
# @celeryd_init.connect
# def app_init(**kwargs):
#     db_client = get_motor_client()
#     loop = get_event_loop()
#     loop.run_until_complete(init_db(db_client))
#     print('\nit ran\n')

celery = get_celery()
celery_logger = get_task_logger(__name__)
