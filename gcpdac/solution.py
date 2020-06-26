# Supports all actions concerning Solutions
import json
import os
from pprint import pformat

import requests
from celery import states
from celery.result import AsyncResult

import config
from gcpdac.celery_tasks import deploy_solution_task, destroy_solution_task
from gcpdac.utils import remove_keys_from_dict

logger = config.logger


def create_async(solutionDetails):
    logger.debug(pformat(solutionDetails))

    result : AsyncResult = deploy_solution_task.delay(solutionDetails=solutionDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    solutionDetails = {"id": oid}

    result : AsyncResult = destroy_solution_task.delay(solutionDetails=solutionDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def create_solution_result(taskid):
    logger.info("CREATE SOLUTION RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["tf_return_code"]
        tf_outputs = retval["tf_outputs"]
        if return_code > 0:
            status = states.FAILURE
            payload = {}
        else:
            payload = tf_outputs
            keys_to_remove = ("billing_account")
            payload = remove_keys_from_dict(payload, keys_to_remove)

        return {'status': status, "payload": json.dumps(payload)}
    else:
        return {'status': status}


def delete_solution_result(taskid):
    logger.info("DELETE SOLUTION RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
        return {'status': status, "tf_return_code": return_code}
    else:
        return {'status': status}

