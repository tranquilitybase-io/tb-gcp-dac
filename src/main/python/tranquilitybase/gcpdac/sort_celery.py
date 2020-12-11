import os

from celery import Celery

from src.main.python.tranquilitybase.celery_worker import celeryconfig


def get_celery():
    global celery_app
    return celery_app


def make_celery(name):
    celery = Celery(
        name,
        backend=os.environ['CELERY_RESULT_BACKEND'],
        broker=os.environ['CELERY_BROKER_URL'],
        config_source=celeryconfig
    )

    return celery


def init_celery():
    global celery_app
    # celeryconfig.init()
    celery_app = make_celery(__name__)
    celery_app.worker_main('worker')
    # celery_worker()


init_celery()