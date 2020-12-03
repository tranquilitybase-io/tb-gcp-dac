# Supports all actions concerning Solutions
import json
from pprint import pformat
from typing import Optional, Any

from celery import states
from celery.result import AsyncResult

import config
from gcpdac.celery_tasks import deploy_solution_task, destroy_solution_task

logger = config.logger


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
    asyncResult: AsyncResult = AsyncResult(taskid)
    status = asyncResult.status
    logger.debug("status {}".format(status))
    payload_dict: dict = {}

    if status == states.FAILURE:
        result: Exception = asyncResult.result
        logger.info("Exception {}".format(result))
        payload_dict["error"] = "Error occurred deploying solution"

    if status == states.SUCCESS:
        # retval: Optional[Any] = asyncResult.get(timeout=1.0)
        retval = asyncResult.result
        logger.debug("retval {}".format(retval))
        if retval != None:
            return_code = retval["tf_return_code"]
            logger.debug("return_code {}".format(return_code))
            payload_dict = retval["tf_outputs"]
            logger.debug("tf_outputs {}".format(payload_dict))
            if return_code > 0:
                logger.debug("return_code > 0")
                payload_dict["error"] = "Return code when deleting: {}".format(return_code)
                status = states.FAILURE
        else:
            logger.debug("retval NONE")
            status = states.FAILURE
            payload_dict["error"] = "No return code from task"

    payload = json.dumps(payload_dict)

    return {'status': status, "payload": payload}


def delete_solution_result(taskid):
    logger.info("DELETE SOLUTION RESULT %s", format(taskid))
    asyncResult = AsyncResult(taskid)
    status = asyncResult.status
    payload_dict = {}

    if status == states.FAILURE:
        result: Exception = asyncResult.result
        logger.info("Exception {}".format(result))
        payload_dict["error"] = "Error occurred deleting solution"

    if status == states.SUCCESS:
        retval = asyncResult.get(timeout=1.0)
        if retval != None:
            return_code = retval["tf_return_code"]
            if return_code > 0:
                payload_dict["error"] = "Return code when deleting: {}".format(return_code)
                status = states.FAILURE

    payload = json.dumps(payload_dict)

    return {'status': status, "payload": payload}
