import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult

from src.main.python.tranquilitybase.celery_worker.celery_tasks import deploy_solution_task, destroy_solution_task


# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))


def create_async(solutionDetails):
    logger.debug(pformat(solutionDetails))
    result: AsyncResult = deploy_solution_task.delay(solutionDetails=solutionDetails)
    logger.info("Task ID %s", result.task_id)
    context = {"taskid": result.task_id}
    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))
    solutionDetails = {"id": oid}
    result: AsyncResult = destroy_solution_task.delay(solutionDetails=solutionDetails)
    logger.info("Task ID %s", result.task_id)
    context = {"taskid": result.task_id}
    return context, 201


def create_solution_result(taskid):
    logger.info("CREATE SOLUTION RESULT %s", format(taskid))
    asyncResult = AsyncResult(taskid)
    status = asyncResult.status
    payload = {}

    if status == states.FAILURE:
        result: Exception = asyncResult.result
        logger.info("Exception {}".format(result))
        # TODO add error message to payload
        payload = {"error": result}

    if status == states.SUCCESS:
        retval = asyncResult.get(timeout=1.0)
        return_code = retval["tf_return_code"]
        tf_outputs = retval["tf_outputs"]
        if return_code > 0:
            status = states.FAILURE
        else:
            payload = tf_outputs
            payload = json.dumps(payload)

    return {'status': status, "payload": payload}


def delete_solution_result(taskid):
    logger.info("DELETE SOLUTION RESULT %s", format(taskid))
    asyncResult = AsyncResult(taskid)
    status = asyncResult.status
    payload = {}

    if status == states.FAILURE:
        result: Exception = asyncResult.result
        logger.info("Exception {}".format(result))
        # TODO add error message to payload

    if status == states.SUCCESS:
        retval = asyncResult.get(timeout=1.0)
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE

    return {'status': status, "payload": payload}
