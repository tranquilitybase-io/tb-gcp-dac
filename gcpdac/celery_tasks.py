import traceback

from celery import states
from celery.exceptions import Ignore

from config import get_celery
from gcpdac.activator_ci import create_activator, delete_activator
from gcpdac.folder_terraform import create_folder, delete_folder
from gcpdac.local_logging import get_logger
from gcpdac.solution_terraform import create_solution, delete_solution

celery_app = get_celery()

logger = get_logger('worker')


class DacTask(celery_app.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info('{0!r} failed: {1!r}'.format(self.task_id, exc))


@celery_app.task(bind=True, base=DacTask, name='deploy_solution')
def deploy_solution_task(self, solutionDetails):
    logger.debug("deploy_solution_task")
    response = create_solution(solutionDetails)
    return_code = response.get("tf_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


@celery_app.task(bind=True, base=DacTask, name='destroy_solution')
def destroy_solution_task(self, solutionDetails):
    logger.debug("destroy_solution_task")
    response = delete_solution(solutionDetails)
    return_code = response.get("tf_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


@celery_app.task(bind=True, base=DacTask, name='create_folder')
def create_folder_task(self, folderDetails):
    logger.debug("create_folder_task")
    response = create_folder(folderDetails)
    return response


@celery_app.task(bind=True, base=DacTask, name='delete_folder')
def delete_folder_task(self, folderDetails):
    logger.debug("delete_folder_task")
    response = delete_folder(folderDetails)
    return_code = response.get("tf_return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


@celery_app.task(bind=True, base=DacTask, name='deploy_activator')
def deploy_activator_task(self, activatorDetails):
    logger.debug("deploy_activator_task")

    try:
        response = create_activator(activatorDetails)
        return_code = response.get("return_code")
        if (return_code) != 0:
            self.update_state(state=states.FAILURE)
        else:
            self.update_state(state=states.SUCCESS)
        return response
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
            })
        raise Ignore()


@celery_app.task(bind=True, base=DacTask, name='destroy_activator')
def destroy_activator_task(self, activatorDetails):
    logger.debug("destroy_activator_task")
    response = delete_activator(activatorDetails)
    return_code = response.get("return_code")
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response
