import json

import requests

from tests.gcp_tests.common_utils import BASE_URL

headers = {'Content-Type': 'application/json'}


def create_activator_task(payload):
    url = '{}/application_async'.format(BASE_URL)
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id


def create_activator_task_result(taskId):
    url = '{}/application_async/result/create/{}'.format(BASE_URL, taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload


def delete_activator_task(activatorId):
    url = '{}/application_async/{}'.format(BASE_URL, activatorId)
    resp = requests.delete(url, headers=headers)

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id


def delete_activator_task_result(taskId):
    url = '{}/application_async/result/delete/{}'.format(BASE_URL, taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload
