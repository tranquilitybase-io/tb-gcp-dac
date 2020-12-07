# Supports all actions concerning Solutions
import os
import logging
import json
from config import app
from config import counter
import random
from pprint import pformat


logger = logging.getLogger("solution")

solution_response_json = ""
solution_response_file = "gcpdac/solution_response_example.json"
with open(solution_response_file, "r") as fh:
    solution_response_json = json.load(fh)

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

def create_async(solutionDetails):
    """
    Return just the task_id.
    """

    logger.debug(pformat(solutionDetails))
    taskid =  next_taskid()
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
    taskid =  next_taskid()
    logger.info("Task ID %s", taskid)
    context = {
        "taskid": f"{taskid}"
    }
    return context, 200


def create_solution_result(taskid):
    logger.info("CREATE SOLUTION RESULT %s",format(taskid))

    retval = {
        "status": get_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(solution_response_json['payload'])
    return retval, 201


def delete_solution_result(taskid):
    logger.info("DELETE SOLUTION RESULT %s",format(taskid))

    retval = {
        "status": get_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(solution_response_json['payload'])
    return retval, 200
