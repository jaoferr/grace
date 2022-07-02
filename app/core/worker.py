from typing import Callable

from celery import Celery

from app.core.config import settings


def get_celery():
    _celery = Celery(__name__)
    _celery.conf.broker_url = settings.assemble_celery_broker_url()
    _celery.conf.result_backend = settings.assemble_celery_broker_url()
    return _celery


celery = get_celery()
