# Supports all actions concerning Solutions
import json
import os
from pprint import pformat

import requests
from flask import abort

import config
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

    result = run_terraform.delay(solutionDetails, 'apply')

    # [logger.debug("%s,%s", key, value) for key, value in result.items()]

    # result.wait()

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

    result = run_terraform.delay(solutionDetails, 'destroy')

    # result.wait()

    context = {"taskid": result.task_id}

    # TODO handle celery failure
    success = True
    if success == True:
        return context, 201
    else:
        abort(500, "Failed to delete your solution")


def successful_deployment_update(solutionId):
    url = "http://" + os.environ['HOUSTON_SERVICE_URL'] + "/api/solutiondeployment/"

    payload = {'id': solutionId, 'deployed': True}
    print(f"url: {url}")
    print(f"data: {payload}")
    headers = {'Content-Type': "application/json"}
    response = requests.put(url + f"/{solutionId}", data=json.dumps(payload), headers=headers)
    print(pformat(response))
    return response
