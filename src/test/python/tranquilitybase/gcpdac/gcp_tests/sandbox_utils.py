import json
import logging

import requests

from gcpdac_tests.gcp_tests.common_utils import BASE_URL

LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

headers = {'Content-Type': 'application/json'}


def create_sandbox_task(payload):
    url = '{}/sandbox_async'.format(BASE_URL)
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id


def create_sandbox_task_result(taskId):
    url = '{}/sandbox_async/result/create/{}'.format(BASE_URL, taskId)
    # convert dict to json by json.dumps() for body data.
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload


def delete_sandbox_task(sandboxId):
    url = '{}/sandbox_async/{}'.format(BASE_URL, sandboxId)
    resp = requests.delete(url, headers=headers)

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id


def delete_sandbox_task_result(taskId):
    url = '{}/sandbox_async/result/delete/{}'.format(BASE_URL, taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload
