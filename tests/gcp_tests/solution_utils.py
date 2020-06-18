import json
import logging

import requests

LOG_LEVEL = logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL

headers = {'Content-Type': 'application/json' }

def create_solution_task(payload):

    url = 'http://localhost:3100/dac/solution_async'
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id

def create_solution_task_result(taskId):

    url = 'http://localhost:3100/dac/solution_async/result/create/{}'.format(taskId)
    # convert dict to json by json.dumps() for body data.
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload

def delete_solution_task(solutionId):

    url = 'http://localhost:3100/dac/solution_async/{}'.format(solutionId)
    resp = requests.delete(url, headers=headers)

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id

def delete_solution_task_result(taskId):

    url = 'http://localhost:3100/dac/solution_async/result/delete/{}'.format(taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload
