import json
import logging

import requests

LOG_LEVEL = logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Additional headers.
headers = {'Content-Type': 'application/json' }

def create_folder_task(folderName, parentFolderId):

    url = 'http://localhost:3100/api/folder_async'
    payload = {"folder": {"folderName": folderName, "parentFolderId": parentFolderId}}

    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id

def create_folder_task_result(taskId):

    url = 'http://localhost:3100/api/folder_async/result/create/{}'.format(taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload

def delete_folder_task(folderName):

    url = 'http://localhost:3100/api/folder_async/{}'.format(folderName)
    resp = requests.delete(url, headers=headers)

    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id

def delete_folder_task_result(taskId):

    url = 'http://localhost:3100/api/folder_async/result/delete/{}'.format(taskId)
    resp = requests.get(url, headers=headers)

    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload
