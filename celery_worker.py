import logging

from config import get_celery
from gcpdac.solution_terraform import run_terraform

celery_app = get_celery()

log = logging.getLogger('worker')
log_format = '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s'
logging.basicConfig(level=logging.INFO,format=log_format)

@celery_app.task()
def add_together_two(a, b):
    return a + b


@celery_app.task()
def deploy_solution_task(solutionDetails):
    run_terraform(solutionDetails, "apply")
    # just return call = True TODO
    return True


@celery_app.task()
def destroy_solution_task(solutionDetails):
    run_terraform(solutionDetails, "destroy")
    # just return call = True TODO
    return True


if __name__ == '__main__':
    celery_app.worker_main('worker')

