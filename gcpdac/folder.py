# Supports all actions concerning Folder 
from pprint import pformat

from celery import states
from celery.result import AsyncResult
from flask import abort

import config
from gcpdac.celery_tasks import create_folder_task, delete_folder_task
from gcpdac.folder_terraform import create_folder, delete_folder

logger = config.logger


def create(folderDetails):
    logger.debug(pformat(folderDetails))

    result = create_folder(folderDetails)
    if result.get("tf_return_code") == 0:
        return result, 201
    else:
        abort(500, "Failed to deploy your folder ")


def delete(oid):
    logger.debug("Id is {}".format(oid))

    folderDetails = {"id": oid}
    result = delete_folder(folderDetails)
    if result.get("tf_return_code") == 0:
        return {}, 200
    else:
        abort(500, "Failed to delete  your folder ")


def create_async(folderDetails):
    logger.debug(pformat(folderDetails))

    result = create_folder_task.delay(folderDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    folderDetails = {"id": oid}

    result = delete_folder_task.delay(folderDetails=folderDetails)

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
        del tf_outputs['folder']['type']
        del tf_outputs['folder']['sensitive']
        return_code = retval["tf_return_code"]
        payload = tf_outputs['folder']['value']
        if return_code > 0:
            status = states.FAILURE
            payload = {}
        return {'status': status, "payload": payload}
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
