# Supports all actions concerning Folder
import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult

import config
from gcpdac.celery_tasks import create_folder_task, delete_folder_task
from gcpdac.utils import remove_keys_from_dict

logger = config.logger


def create_async(folderDetails):
    logger.debug(pformat(folderDetails))

    result: AsyncResult = create_folder_task.delay(folderDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    folderDetails = {"id": oid}

    result : AsyncResult = delete_folder_task.delay(folderDetails=folderDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def create_folder_result(taskid):
    logger.info("CREATE FOLDER RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        logger.debug("retval %s", retval)
        tf_outputs: dict = retval["tf_outputs"]
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
            payload = {}
        else:
            payload = tf_outputs
            keys_to_remove = ("billing_account")
            remove_keys_from_dict(payload, keys_to_remove)
        return {'status': status, "payload": json.dumps(payload)}
    else:
        return {'status': status}


def delete_folder_result(taskid):
    logger.info("DELETE FOLDER RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
        return {'status': status}
    else:
        return {'status': status}
