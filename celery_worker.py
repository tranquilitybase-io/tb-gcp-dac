import logging

from celery import signals

from config import get_celery
from gcpdac.solution_terraform import run_terraform

celery_app = get_celery()

logger = logging.getLogger('worker')
log_format = '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s'
logging.basicConfig(level=logging.INFO, format=log_format)

@celery_app.task()
def add_two_numbers(a, b):
    logger.debug("add %s + %s", a, b)
    return a + b


@celery_app.task()
def deploy_solution_task(solutionDetails):
    logger.debug("deploy_solution_task")
    response = run_terraform(solutionDetails, "apply")
    return response


@celery_app.task()
def destroy_solution_task(solutionDetails):
    logger.debug("destroy_solution_task")
    response = run_terraform(solutionDetails, "destroy")
    return response

# DON'T REMOVE - added to fix celery logging error
@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


if __name__ == '__main__':
    celery_app.worker_main('worker')
