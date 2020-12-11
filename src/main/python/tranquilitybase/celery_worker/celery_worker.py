import os

from celery import signals, Celery

from src.main.python.tranquilitybase.celery_worker import celeryconfig
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger

logger = get_logger('worker')
global celery_app


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


def make_celery(name):
    celery = Celery(
        name,
        backend=os.environ['CELERY_RESULT_BACKEND'],
        broker=os.environ['CELERY_BROKER_URL'],
        config_source=celeryconfig
    )

    return celery


celery_app = make_celery(__name__)

def get_celery():
    return celery_app

if __name__ == '__main__':
    celery_app.worker_main('worker')
