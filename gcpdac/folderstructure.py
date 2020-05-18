# Supports all actions concerning Folder Structure
from pprint import pformat

from celery import states
from celery.result import AsyncResult
from flask import abort

import config
from gcpdac.celery_tasks import deploy_folderstructure_task, destroy_folderstructure_task
from gcpdac.folderstructure_terraform import run_terraform

logger = config.logger


def create(folderstructureDetails):
    logger.debug(pformat(folderstructureDetails))

    result = run_terraform(folderstructureDetails, "apply")
    if result.get("tf_return_code") == 0:
        return result, 201
    else:
        abort(500, "Failed to deploy your folder structure")


def delete(oid):
    logger.debug("Id is {}".format(oid))

    folderstructureDetails = {"id": oid}
    result = run_terraform(folderstructureDetails, "destroy")
    if result.get("tf_return_code") == 0:
        return {}, 200
    else:
        abort(500, "Failed to delete  your folder structure")


def create_async(folderstructureDetails):
    logger.debug(pformat(folderstructureDetails))

    result = deploy_folderstructure_task.delay(folderstructureDetails=folderstructureDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    # TODO handle celery failure
    success = True
    if success == True:
        return context, 201
    else:
        abort(500, "Failed to create your solution")


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    folderstructureDetails = {"id": oid}

    result = destroy_folderstructure_task.delay(folderstructureDetails=folderstructureDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    # TODO handle celery failure
    success = True
    if success == True:
        return context, 201
    else:
        abort(500, "Failed to delete your folder structure")


def create_folderstructure_result(taskid):
    logger.info("CREATE FOLDER STRUCTURE RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        tf_state = retval["tf_state"]
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
        return {'status': status, "tf_state": tf_state, "tf_return_code": return_code}
    else:
        return {'status': status}


def delete_folderstructure_result(taskid):
    logger.info("DELETE FOLDER STRUCTURE RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
        return {'status': status, "tf_return_code": return_code}
    else:
        return {'status': status}


