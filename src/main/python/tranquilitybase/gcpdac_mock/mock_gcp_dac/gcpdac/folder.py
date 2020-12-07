# Supports all actions concerning Solutions
import os
import logging
import json
from config import app
from config import counter
import random
from pprint import pformat


logger = logging.getLogger("folder")

folder_response_json = ""
folder_response_file = "gcpdac/folder_response_example.json"
with open(folder_response_file, "r") as fh:
    folder_response_json = json.load(fh)

def next_taskid():
    task_cnt = next(counter)
    taskid = f"MOCKTASKID{task_cnt}"
    return taskid


def next_folderid():
    folder_cnt = next(counter)
    folderid = f"MOCKFOLDERID{folder_cnt}"
    return folderid


def get_random_status():
    r = random.randint(0, 10)
    if r == 0:
        status = "FAILURE"
    elif r in (1, 2, 3, 4):
        status = "STARTED"
    elif r > 4:
        status = "SUCCESS"
    return status


def get_status():
    if os.environ.get("MOCK_MODE"):
        return get_random_status()
    else:
        return "SUCCESS"


def create_async(folderDetails):
    """
    Return just the task_id.
    """

    logger.debug(pformat(folderDetails))
    taskid = next_taskid()
    logger.info("Task ID %s", taskid)
    context = {
        "taskid": f"{taskid}"
    }
    return context, 201


def delete_async(oid):
    """
    Return just the task_id.
    """
    logger.debug("Id is {}".format(oid))
    taskid = next_taskid()
    logger.info("Task ID %s", taskid)
    context = {
        "taskid": f"{taskid}"
    }
    return context, 200


def create_folder_result(taskid):
    logger.info("CREATE FOLDER RESULT %s", format(taskid))

    retval = {}
    status = get_status()
    retval["status"] = status

    if status == "SUCCESS":
        folderid = next_folderid()
        payload = folder_response_json['payload']
        payload["folder"]["value"]["id"] = folderid
        retval['payload'] = json.dumps(payload)
    return retval, 201


def delete_folder_result(taskid):
    logger.info("DELETE FOLDER RESULT %s", format(taskid))

    retval = {}
    status = get_status()
    retval["status"] = status

    if status == "SUCCESS":
        retval['payload'] = json.dumps(folder_response_json['payload'])

    return retval, 200
