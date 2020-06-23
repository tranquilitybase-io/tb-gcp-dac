# Supports all actions concerning applications
import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult
from flask import abort

import config
from gcpdac.activator_ci import create_activator, delete_activator
from gcpdac.celery_tasks import deploy_activator_task, destroy_activator_task

logger = config.logger


def create(activatorDetails):
    logger.debug(pformat(activatorDetails))

    result = create_activator(activatorDetails)
    if result.get("tf_return_code") == 0:
        return result, 201
    else:
        abort(500, "Failed to deploy your activator")


def delete(oid):
    logger.debug("Id is {}".format(oid))

    activatorDetails = {"id": oid}
    result = delete_activator(activatorDetails)
    if result.get("tf_return_code") == 0:
        return {}, 200
    else:
        abort(500, "Failed to delete  your activator")


def create_async(activatorDetails):
    logger.debug(pformat(activatorDetails))

    result = deploy_activator_task.delay(activatorDetails=activatorDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    # TODO handle celery failure
    success = True
    if success == True:
        return context, 201
    else:
        abort(500, "Failed to create your activator")


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    activatorDetails = {"id": oid}

    result = destroy_activator_task.delay(activatorDetails=activatorDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    # TODO handle celery failure
    success = True
    if success == True:
        return context, 201
    else:
        abort(500, "Failed to delete your activator")


def create_activator_result(taskid):
    logger.info("CREATE activator RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["return_code"]
        # tf_outputs = retval["tf_outputs"]
        if return_code > 0:
            status = states.FAILURE
            payload = {}
        else:
            payload = {}

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


