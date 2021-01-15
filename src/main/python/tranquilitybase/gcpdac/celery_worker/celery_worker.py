from src.main.python.tranquilitybase.gcpdac.celery_worker import celery_access
from src.main.python.tranquilitybase.gcpdac.configuration import config

config.init()
celery = celery_access.get_celery()
