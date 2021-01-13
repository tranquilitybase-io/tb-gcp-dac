from celery import signals, Celery

from src.main.python.tranquilitybase.gcpdac.celery_worker import celeryconfig
from src.main.python.tranquilitybase.gcpdac.configuration import config



@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


def make_celery(name):
    celery = Celery(
        name,
        backend="redis://redis:6379",         # os.environ['CELERY_RESULT_BACKEND'],
        broker="redis://redis:6379",     # os.environ['CELERY_BROKER_URL']
        config_source=celeryconfig
    )

    return celery


celery_app = make_celery(__name__)


def get_celery():
    return celery_app


config.init()

if __name__ == '__main__':
    celery_app.worker_main('worker')
