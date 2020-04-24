# Supports all actions concerning Solutions
import json
import os
import requests
from flask import abort
from pprint import pformat
from gcpdac.local_logging import get_logger
from gcpdac.solution_terraform import run_terraform

logger = get_logger()
logger.info("Logger initialised")


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


def successful_deployment_update(solutionId):
    url = "http://" + os.environ['HOUSTON_SERVICE_URL'] + "/api/solutiondeployment/"

    payload = {'id': solutionId, 'deployed': True}
    print(f"url: {url}")
    print(f"data: {payload}")
    headers = {'Content-Type': "application/json"}
    response = requests.put(url + f"/{solutionId}", data=json.dumps(payload), headers=headers)
    print(pformat(response))
    return response
