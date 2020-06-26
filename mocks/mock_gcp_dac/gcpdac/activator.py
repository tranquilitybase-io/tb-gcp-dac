# Supports all actions concerning activators
import json
import random
from pprint import pformat

from config import app
from config import counter

activator_response_json = ""
activator_response_file = "gcpdac/activator_response_example.json"
with open(activator_response_file, "r") as fh:
    activator_response_json = json.load(fh)

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


def create_async(activatorDetails):
    """
    Return just the task_id.
    """

    app.logger.debug(pformat(activatorDetails))
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


def create_activator_result(taskid):
    app.logger.info("CREATE activator RESULT %s",format(taskid))
    print(f"taskid: {taskid}")

    retval = {
        "status": get_random_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(activator_response_json['payload'])
    return retval, 201


def delete_activator_result(taskid):
    app.logger.info("DELETE activator RESULT %s",format(taskid))
    print(f"taskid: {taskid}")

    retval = {
        "status": get_random_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(activator_response_json['payload'])
    return retval, 200
