# Supports all actions concerning sandboxes
import json
import logging
import os
import random
from pprint import pformat

from config import counter

logger = logging.getLogger("sandbox")

sandbox_response_json = ""
sandbox_response_file = "gcpdac/sandbox_response_example.json"
with open(sandbox_response_file, "r") as fh:
    sandbox_response_json = json.load(fh)


def next_taskid():
    task_cnt = next(counter)
    taskid = f"MOCKTASKID{task_cnt}"
    return taskid


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


def create_async(sandboxDetails):
    logger.debug(pformat(sandboxDetails))
    taskid = next_taskid()
    logger.info("Task ID %s", taskid)
    context = {
        "taskid": f"{taskid}"
    }
    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))
    taskid = next_taskid()
    logger.info("Task ID %s", taskid)
    context = {
        "taskid": f"{taskid}"
    }
    return context, 200


def create_sandbox_result(taskid):
    logger.info("CREATE sandbox RESULT %s", format(taskid))

    retval = {
        "status": get_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(sandbox_response_json['payload'])
    return retval, 201


def delete_sandbox_result(taskid):
    logger.info("DELETE sandbox RESULT %s", format(taskid))

    retval = {
        "status": get_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(sandbox_response_json['payload'])
    return retval, 200
