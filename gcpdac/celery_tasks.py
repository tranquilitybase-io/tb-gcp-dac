from celery import states

from config import get_celery
from gcpdac.folder_terraform import create_folder, delete_folder
from gcpdac.local_logging import get_logger
from gcpdac.solution_terraform import create_solution

celery_app = get_celery()

logger = get_logger('worker')

@celery_app.task(bind=True)
def deploy_solution_task(self, solutionDetails):
    logger.debug("deploy_solution_task")
    response = create_solution(solutionDetails, "apply")
    return_code = response.get("tf_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


@celery_app.task(bind=True)
def destroy_solution_task(self, solutionDetails):
    logger.debug("destroy_solution_task")
    response = create_solution(solutionDetails, "destroy")
    return_code = response.get("tf_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response

@celery_app.task(bind=True)
def deploy_folder_task(self, folderDetails):
    logger.debug("deploy_folder_task")
    response_all = dict()
    count = 1
    for folder in folderDetails.get("folder"):
        logger.debug("folder {}".format(folder))
        response = create_folder(folder)
        response_key = "response{}".format(count)
        response_all[response_key] = response
        count += 1

    return response_all


@celery_app.task(bind=True)
def destroy_folder_task(self, folderDetails):
    logger.debug("destroy_folder_task")
    response = delete_folder(folderDetails)
    return_code = response.get("tf_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


