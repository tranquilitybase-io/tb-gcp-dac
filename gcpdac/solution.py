# Supports all actions concerning Solutions
import json
import os
from pprint import pformat

import requests
from celery import states
from celery.result import AsyncResult
from flask import abort

import config
from  gcpdac.celery_tasks import deploy_solution_task, destroy_solution_task
from gcpdac.solution_terraform import run_terraform

logger = config.logger


def create(solutionDetails):
    logger.debug(pformat(solutionDetails))

    # TODO populate with data as well as True/False
    result = run_terraform(solutionDetails, "apply")
    if result.get("return_code") == 0:
        success = True
    else:
        success = False

    if success == True:
        # TODO populate from run_terraform
        data = {}
        return data, 201
    else:
        abort(500, "Failed to deploy your solution")


def delete(oid):
    logger.debug("Id is {}".format(oid))

    solutionDetails = {"id": oid}
    result = run_terraform(solutionDetails, "destroy")
    if result.get("return_code") == 0:
        success = True
    else:
        success = False

    if success == True:
        return {}, 200
    else:
        abort(500, "Failed to delete  your solution")


def create_async(solutionDetails):
    logger.debug(pformat(solutionDetails))

    result = deploy_solution_task.delay(solutionDetails=solutionDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    # TODO handle celery failure
    success = True
    if success == True:
        return context, 201
    else:
        abort(500, "Failed to delete your solution")


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    solutionDetails = {"id": oid}

    result = destroy_solution_task.delay(solutionDetails=solutionDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    # TODO handle celery failure
    success = True
    if success == True:
        return context, 201
    else:
        abort(500, "Failed to delete your solution")


def create_solution_result(taskid):
    logger.info("CREATE SOLUTION RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        tf_state = retval["tf_state"]
        return_code = retval["terraform_return_code"]
        return {'status': status, "tf_state": tf_state, "terraform_return_code": return_code}
    else:
        return {'status': status}


def delete_solution_result(taskid):
    logger.info("DELETE SOLUTION RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["terraform_return_code"]
        return {'status': status, "terraform_return_code": return_code}
    else:
        return {'status': status}


def successful_deployment_update(solutionId):
    url = "http://" + os.environ['HOUSTON_SERVICE_URL'] + "/api/solutiondeployment/"

    payload = {'id': solutionId, 'deployed': True}
    print(f"url: {url}")
    print(f"data: {payload}")
    headers = {'Content-Type': "application/json"}
    response = requests.put(url + f"/{solutionId}", data=json.dumps(payload), headers=headers)
    print(pformat(response))
    return response
