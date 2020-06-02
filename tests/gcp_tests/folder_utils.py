import json
import logging

import requests

LOG_LEVEL = logging.INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Additional headers.
headers = {'Content-Type': 'application/json' }

def create_folder_task(folderName, parentFolderId):

    #Test POST Then GET
    # Body
    url = 'http://localhost:3100/api/folder_async'
    payload = {"folder": {"folderName": folderName, "parentFolderId": parentFolderId}}
    # convert dict to json by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload,indent=4))

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id

def create_folder_task_result(taskId):

    url = 'http://localhost:3100/api/folder_async/result/create/{}'.format(taskId)
    # convert dict to json by json.dumps() for body data.
    resp = requests.get(url, headers=headers)

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload

def delete_folder_task(folderName):

    # Body
    url = 'http://localhost:3100/api/folder_async/{}'.format(folderName)
    # convert dict to json by json.dumps() for body data.
    resp = requests.delete(url, headers=headers)

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    task_id = resp_json['taskid']

    return task_id

def delete_folder_task_result(taskId):

    url = 'http://localhost:3100/api/folder_async/result/delete/{}'.format(taskId)
    # convert dict to json by json.dumps() for body data.
    resp = requests.get(url, headers=headers)

    # Validate response headers and body contents, e.g. status code.
    resp_json = resp.json()
    status = resp_json['status']
    payload = resp_json.get('payload', None)

    return status, payload
