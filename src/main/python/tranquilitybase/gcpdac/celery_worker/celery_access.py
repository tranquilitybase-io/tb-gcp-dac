from celery import signals, Celery
from src.main.python.tranquilitybase.gcpdac.celery_worker import celeryconfig

global celery_app


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


def make_celery(name: str, backend: str, broker: str):

    celery = Celery(
        name,
        backend=backend,
        broker=broker,
        config_source=celeryconfig
    )

    return celery


def get_celery():
    global celery_app
    return celery_app


def set_celery(backend, broker):
    global celery_app
    celery_app = make_celery(__name__, backend, broker)
