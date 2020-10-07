# Supports all actions concerning applications
import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult

import config
from gcpdac.celery_tasks import deploy_application_task, destroy_application_task

logger = config.logger


def create_async(applicationDetails):
    logger.debug(pformat(applicationDetails))

    result: AsyncResult = deploy_application_task.delay(applicationDetails=applicationDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    applicationDetails = {"id": oid}

    result: AsyncResult = destroy_application_task.delay(applicationDetails=applicationDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def create_application_result(taskid):
    logger.info("CREATE application RESULT %s", format(taskid))
    asyncResult: AsyncResult = AsyncResult(taskid)
    status = asyncResult.status
    payload = {}

    if status == states.FAILURE:
        result: Exception = asyncResult.result
        logger.info("Exception {}".format(result))
        # TODO add error message to payload

    if status == states.SUCCESS:
        retval = asyncResult.get(timeout=1.0)
        return_code = retval["return_code"]
        payload = json.dumps(retval["payload"])
        if return_code > 0:
            status = states.FAILURE

    return {'status': status, "payload": payload}


def delete_application_result(taskid):
    logger.info("DELETE application RESULT %s", format(taskid))
    asyncResult = AsyncResult(taskid)
    status = asyncResult.status
    payload = {}

    if status == states.FAILURE:
        result: Exception = asyncResult.result
        logger.info("Exception {}".format(result))

    if status == states.SUCCESS:
        retval = asyncResult.get(timeout=1.0)
        return_code = retval["return_code"]
        if return_code > 0:
            status = states.FAILURE
        payload["return_code"] = return_code

    return {'status': status, "payload": payload}
