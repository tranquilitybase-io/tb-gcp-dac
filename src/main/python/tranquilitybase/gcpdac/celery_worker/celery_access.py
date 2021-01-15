from celery import signals, Celery
from src.main.python.tranquilitybase.gcpdac.celery_worker import celeryconfig
from src.main.python.tranquilitybase.gcpdac.configuration import config

global celery_app


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


def make_celery():
    celery = Celery(
        __name__,
        backend=config.environment_helper.get_celery_result_backend(),
        broker=config.environment_helper.get_celery_broker_url(),
        config_source=celeryconfig
    )

    return celery


def get_celery():
    global celery_app

    try:
        celery_app
    except Exception as e:
        celery_app = make_celery()

    return celery_app


