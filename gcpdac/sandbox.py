# Supports all actions concerning sandboxes
import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult

import config
from gcpdac.celery_tasks import deploy_sandbox_task, destroy_sandbox_task

logger = config.logger


def create_async(sandboxDetails):
    logger.debug(pformat(sandboxDetails))
    # TODO implement
    return {}, 201
    # result: AsyncResult = deploy_sandbox_task.delay(sandboxDetails=sandboxDetails)
    #
    # logger.info("Task ID %s", result.task_id)
    #
    # context = {"taskid": result.task_id}
    #
    # return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    sandboxDetails = {"id": oid}
    # TODO implement
    return {}, 201

    # result: AsyncResult = destroy_sandbox_task.delay(sandboxDetails=sandboxDetails)
    #
    # logger.info("Task ID %s", result.task_id)
    #
    # context = {"taskid": result.task_id}
    #
    # return context, 201


def create_sandbox_result(taskid):
    logger.info("CREATE SANDBOX RESULT %s", format(taskid))
    # TODO implement
    return {}

    # asyncResult = AsyncResult(taskid)
    # status = asyncResult.status
    # payload = {}
    #
    # if status == states.FAILURE:
    #     result: Exception = asyncResult.result
    #     logger.info("Exception {}".format(result))
    #     # TODO add error message to payload
    #     # payload = {"error": result}
    #
    # if status == states.SUCCESS:
    #     retval = asyncResult.get(timeout=1.0)
    #     return_code = retval["tf_return_code"]
    #     tf_outputs = retval["tf_outputs"]
    #     if return_code > 0:
    #         status = states.FAILURE
    #     else:
    #         payload = tf_outputs
    #         payload = json.dumps(payload)
    #
    # return {'status': status, "payload": payload}
    #

def delete_sandbox_result(taskid):
    logger.info("DELETE SANDBOX RESULT %s", format(taskid))
    # TODO implement
    return {}
    # asyncResult = AsyncResult(taskid)
    # status = asyncResult.status
    # payload = {}
    #
    # if status == states.FAILURE:
    #     result: Exception = asyncResult.result
    #     logger.info("Exception {}".format(result))
    #     # TODO add error message to payload
    #
    # if status == states.SUCCESS:
    #     retval = asyncResult.get(timeout=1.0)
    #     return_code = retval["tf_return_code"]
    #     if return_code > 0:
    #         status = states.FAILURE
    #
    # return {'status': status, "payload": payload}
