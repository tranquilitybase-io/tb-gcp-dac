import os

from celery import Celery

from src.main.python.tranquilitybase.celery_worker import celeryconfig

global celery_app


def validate():
    pass


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
    # celery_app.worker_main('worker')
    # celery_worker()


init_celery()


from src.main.python.tranquilitybase.celery_worker import celery_tasks

task_track_started = True
task_ignore_result = False

celery_tasks.validate()
imports = 'celery_tasks'
print("===========")


# if __name__ == '__main__':
#     celery_tasks.validate()
#
#
#     print("=====CELAREY======")
#     print("=====CELAREY======")
#     print("=====CELAREY======")
#     print("=====CELAREY======")