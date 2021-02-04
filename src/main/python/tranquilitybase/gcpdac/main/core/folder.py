import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult
from src.main.python.tranquilitybase.gcpdac.celery_worker.celery_tasks import create_folder_task, delete_folder_task

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger, get_frame_name
logger = get_logger(get_frame_name(inspect.currentframe()))


def create_async(folderDetails):
    logger.debug(pformat(folderDetails))
    result: AsyncResult = create_folder_task.delay(folderDetails)
    logger.info("Task ID %s", result.task_id)
    context = {"taskid": result.task_id}
    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))
    folderDetails = {"id": oid}
    result: AsyncResult = delete_folder_task.delay(folderDetails=folderDetails)
    logger.info("Task ID %s", result.task_id)
    context = {"taskid": result.task_id}
    return context, 201


def create_folder_result(taskid):
    logger.info("CREATE FOLDER RESULT %s", format(taskid))
    asyncResult = AsyncResult(taskid)
    status = asyncResult.status
    payload = {}

    if status == states.FAILURE:
        result: Exception = asyncResult.result
        logger.info("Exception {}".format(result))
        # TODO add error message to payload

    if status == states.SUCCESS:
        retval = asyncResult.get(timeout=1.0)
        logger.debug("retval %s", retval)
        tf_outputs: dict = retval["tf_outputs"]
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
        else:
            payload = tf_outputs
            payload = json.dumps(payload)

    return {'status': status, "payload": payload}


def delete_folder_result(taskid):
    logger.info("DELETE FOLDER RESULT %s", format(taskid))
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
