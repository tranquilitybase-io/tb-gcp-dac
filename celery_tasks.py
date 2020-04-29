import os

from celery import Celery

import config

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.environ['CELERY_RESULT_BACKEND'],
        broker=os.environ['CELERY_BROKER_URL']
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(config.app)


@celery.task()
def add_together(a, b):
    return a + b
