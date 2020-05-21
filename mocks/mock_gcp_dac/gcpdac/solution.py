# Supports all actions concerning Solutions
import json
from pprint import pformat
from config import app
from config import counter
import random


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


def create_async(solutionDetails):
    """
    Return just the task_id.
    """

    app.logger.debug(pformat(solutionDetails))
    taskid =  next_taskid()
    app.logger.info("Task ID %s", taskid)
    context = {
        "taskid": f"{taskid}"
    }
    return context, 201


def delete_async(oid):
    """
    Return just the task_id.
    """
    app.logger.debug("Id is {}".format(oid))
    taskid =  next_taskid()
    app.logger.info("Task ID %s", taskid)
    context = {
        "taskid": f"{taskid}"
    }
    return context, 200


def create_solution_result(taskid):
    app.logger.info("CREATE SOLUTION RESULT %s",format(taskid))
    print(f"taskid: {taskid}")

    retval = {
        "status": get_random_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(solution_response_json['payload'])
    return retval, 201


def delete_solution_result(taskid):
    app.logger.info("DELETE SOLUTION RESULT %s",format(taskid))
    print(f"taskid: {taskid}")

    retval = {
        "status": get_random_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(solution_response_json['payload'])
    return retval, 200
