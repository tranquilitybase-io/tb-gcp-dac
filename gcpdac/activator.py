# Supports all actions concerning applications
import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult

import config
from gcpdac.celery_tasks import deploy_activator_task, destroy_activator_task

logger = config.logger


def create_async(activatorDetails):
    logger.debug(pformat(activatorDetails))

    result: AsyncResult = deploy_activator_task.delay(activatorDetails=activatorDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    activatorDetails = {"id": oid}

    result: AsyncResult = destroy_activator_task.delay(activatorDetails=activatorDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def create_activator_result(taskid):
    logger.info("CREATE activator RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["return_code"]
        payload = {}
        payload["repo_name"] = retval["repo_name"]
        if return_code > 0:
            status = states.FAILURE

        return {'status': status, "payload": json.dumps(payload)}
    else:
        return {'status': status}


def delete_activator_result(taskid):
    logger.info("DELETE activator RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["return_code"]
        if return_code > 0:
            status = states.FAILURE
        return {'status': status, "return_code": return_code}
    else:
        return {'status': status}
