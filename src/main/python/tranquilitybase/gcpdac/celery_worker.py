from celery import signals

from config import get_celery
from tb_common.local_logging import get_logger

celery_app = get_celery()

logger = get_logger('worker')


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


if __name__ == '__main__':
    celery_app.worker_main('worker')
