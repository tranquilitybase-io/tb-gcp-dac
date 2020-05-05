from celery import states

from config import get_celery
from gcpdac.local_logging import get_logger
from gcpdac.solution_terraform import run_terraform

celery_app = get_celery()

logger = get_logger('worker')

@celery_app.task()
def add_two_numbers(a, b):
    logger.debug("add %s + %s", a, b)
    return a + b


@celery_app.task(bind=True)
def deploy_solution_task(self, solutionDetails):
    logger.debug("deploy_solution_task")
    response = run_terraform(solutionDetails, "apply")
    return_code = response.get("terraform_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


@celery_app.task(bind=True)
def destroy_solution_task(self, solutionDetails):
    logger.debug("destroy_solution_task")
    response = run_terraform(solutionDetails, "destroy")
    return_code = response.get("terraform_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


