from celery import Celery

from src.main.python.tranquilitybase.gcpdac import config
from src.main.python.tranquilitybase.gcpdac.celery import celeryconfig

global celery_app


def get_celery():
    global celery_app
    return celery_app


def init():
    global celery_app
    celery_app = Celery(
            __name__,
            backend=config.environment_helper.get_celery_result_backend(),
            broker=config.environment_helper.get_celery_broker_url(),
            config_source=celeryconfig)


