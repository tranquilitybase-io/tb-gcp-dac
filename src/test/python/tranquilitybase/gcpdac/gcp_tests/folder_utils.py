import json
import logging

import requests
from gcpdac_tests.gcp_tests.common_utils import BASE_URL

LOG_LEVEL = logging.INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Additional headers.
headers = {'Content-Type': 'application/json'}


def create_folder_task(folderName, parentFolderId):
    url = '{}/folder_async'.format(BASE_URL)
    payload = {"folder": {"folderName": folderName, "parentFolderId": parentFolderId}}

    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id


def create_folder_task_result(taskId):
    url = '{}/folder_async/result/create/{}'.format(BASE_URL, taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload


def delete_folder_task(folderName):
    url = '{}/folder_async/{}'.format(BASE_URL, folderName)
    resp = requests.delete(url, headers=headers)

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id


def delete_folder_task_result(taskId):
    url = '{}/folder_async/result/delete/{}'.format(BASE_URL, taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']

    return status
