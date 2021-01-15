from src.main.python.tranquilitybase.gcpdac.celery_worker import celery_access
from src.main.python.tranquilitybase.gcpdac.configuration import config

config.init()
celery_access.set_celery(backend=config.environment_helper.get_celery_result_backend(),
                         broker=config.environment_helper.get_celery_broker_url())

celery = celery_access.get_celery()
