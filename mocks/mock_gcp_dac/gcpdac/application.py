# Supports all actions concerning Applications
import json
from pprint import pformat
from config import app
from config import counter
import random


application_response_json = ""
application_response_file = "gcpdac/application_response_example.json"
with open(application_response_file, "r") as fh:
    application_response_json = json.load(fh)

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


def create_async(applicationDetails):
    """
    Return just the task_id.
    """

    app.logger.debug(pformat(applicationDetails))
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


def create_application_result(taskid):
    app.logger.info("CREATE APPLICATION RESULT %s",format(taskid))
    print(f"taskid: {taskid}")

    retval = {
        "status": get_random_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(application_response_json['payload'])
    return retval, 201


def delete_application_result(taskid):
    app.logger.info("DELETE APPLICATION RESULT %s",format(taskid))
    print(f"taskid: {taskid}")

    retval = {
        "status": get_random_status()
    }
    if retval.get('status') == "SUCCESS" or retval.get('status') == "FAILURE":
        retval["payload"] = json.dumps(application_response_json['payload'])
    return retval, 200
