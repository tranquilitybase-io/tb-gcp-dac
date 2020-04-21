"""
This is the solution module and supports all the ReST actions for the
solution collection
"""
from flask import abort
import os
import requests
import json
from pprint import pformat
from gcpdac.terraform import run_terraform
from pprint import pprint
from gcpdac import models

def create(solutionDetails):
    print(pformat(solutionDetails))

    # mkdir Folders/Projects
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

def successful_deployment_update(id):
    url = "http://" + os.environ['HOUSTON_SERVICE_URL'] + "/api/solutiondeployment/"

    payload = {'id': id, 'deployed': True}
    print(f"url: {url}")
    print(f"data: {payload}")
    headers = {'Content-Type': "application/json"}
    response = requests.put(url + f"/{id}", data=json.dumps(payload), headers=headers)
    print(pformat(response))
    return response
