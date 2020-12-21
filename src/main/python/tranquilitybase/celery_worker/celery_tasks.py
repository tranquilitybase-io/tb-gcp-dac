
# from src.main.python.tranquilitybase.gcpdac.core.todo.solution_terraform import create_solution
from src.main.python.tranquilitybase.gcpdac.core.terraform.solution_terraform import create_solution
from src.main.python.tranquilitybase.gcpdac.sort_celery import get_celery
from celery import states

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))


dry_run = True


def validate():
    pass


celery_app = get_celery()
print("celery_app::::: " + str(celery_app))


class DacTask(celery_app.Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info('{0!r} failed: {1!r}'.format(self.task_id, exc))


@celery_app.task(bind=True, base=DacTask, name='deploy_solution')
def deploy_solution_task(self, solutionDetails):
    logger.debug("deploy_solution_task")
    response = create_solution(solutionDetails)
    return_code = response.get("tf_return_code")
    # response = ""
    # return_code = 0
    if (return_code) != 0:
        self.update_state(state=states.FAILURE)
    else:
        self.update_state(state=states.SUCCESS)
    return response


@celery_app.task(bind=True, base=DacTask, name='destroy_solution')
def destroy_solution_task(self, solutionDetails):
    # logger.debug("destroy_solution_task")
    # response = delete_solution(solutionDetails)
    # return_code = response.get("tf_return_code")
    # if (return_code) != 0:
    #     self.update_state(state=states.FAILURE)
    # else:
    #     self.update_state(state=states.SUCCESS)
    # return response
    pass


# @celery_app.task(bind=True, base=DacTask, name='deploy_sandbox')
# def deploy_sandbox_task(self, sandboxDetails):
#     logger.debug("deploy_sandbox_task")
#     response = create_sandbox(sandboxDetails)
#     return_code = response.get("tf_return_code")
#     if (return_code) != 0:
#         self.update_state(state=states.FAILURE)
#     else:
#         self.update_state(state=states.SUCCESS)
#     return response
#
#
# @celery_app.task(bind=True, base=DacTask, name='destroy_sandbox')
# def destroy_sandbox_task(self, sandboxDetails):
#     logger.debug("destroy_sandbox_task")
#     response = delete_sandbox(sandboxDetails)
#     return_code = response.get("tf_return_code")
#     if (return_code) != 0:
#         self.update_state(state=states.FAILURE)
#     else:
#         self.update_state(state=states.SUCCESS)
#     return response
#
#
# @celery_app.task(bind=True, base=DacTask, name='create_folder')
# def create_folder_task(self, folderDetails):
#     logger.debug("create_folder_task")
#     response = create_folder(folderDetails)
#     return response
#
#
# @celery_app.task(bind=True, base=DacTask, name='delete_folder')
# def delete_folder_task(self, folderDetails):
#     logger.debug("delete_folder_task")
#     response = delete_folder(folderDetails)
#     return_code = response.get("tf_return_code")
#     if (return_code) != 0:
#         self.update_state(state=states.FAILURE)
#     else:
#         self.update_state(state=states.SUCCESS)
#     return response
#
#
@celery_app.task(bind=True, base=DacTask, name='deploy_application')
def deploy_application_task(self, applicationDetails):
    print("DODODODODDODODODODODODODOOITTITITITII")
    print("DODODODODDODODODODODODODOOITTITITITII")
    print("DODODODODDODODODODODODODOOITTITITITII")
    print("DODODODODDODODODODODODODOOITTITITITII")
    print("DODODODODDODODODODODODODOOITTITITITII")
    logger.debug("deploy_application_task")
    return "response"
    # try:
    #     response = create_application(applicationDetails)
    #     return_code = response.get("return_code")
    #     if (return_code) != 0:
    #         self.update_state(state=states.FAILURE)
    #     else:
    #         self.update_state(state=states.SUCCESS)
    #     return response
    # except Exception as ex:
    #     self.update_state(
    #         state=states.FAILURE,
    #         meta={
    #             'exc_type': type(ex).__name__,
    #             'exc_message': traceback.format_exc().split('\n')
    #         })
    #     raise Ignore()
#
#
# @celery_app.task(bind=True, base=DacTask, name='destroy_application')
# def destroy_application_task(self, applicationDetails):
#     logger.debug("destroy_application_task")
#     response = delete_application(applicationDetails)
#     return_code = response.get("return_code")
#     if (return_code) != 0:
#         self.update_state(state=states.FAILURE)
#     else:
#         self.update_state(state=states.SUCCESS)
#     return response
