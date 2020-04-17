from flask import abort
import os
import requests
import json
from pprint import pformat

def create(solutionDetails):
    print(pformat(solutionDetails))

    # mkdir Folders/Projects

    # skeleton code 
    success = True

    if success == True:
        data = { }
        return  data, 201
    else:
        abort(500, "Failed to deploy your solution")


def successful_deployment_update(id):

    url = "http://" + os.environ['HOUSTON_SERVICE_URL'] + "/api/solutiondeployment/"

    payload = { 'id': id, 'deployed': True }
    print(f"url: {url}")
    print(f"data: {payload}")
    headers = { 'Content-Type': "application/json" }
    response = requests.put(url + f"/{id}", data=json.dumps(payload), headers=headers)
    print(pformat(response))
    return response

