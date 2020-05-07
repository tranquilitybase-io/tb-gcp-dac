# Supports all actions concerning Solutions
import json
import os
from pprint import pformat
import requests
from flask import abort
import json
from config import app
from config import counter

my_json = {'lineage': '7b590a8c-e4be-d8c6-6e00-57abbdfd3c3c',
 'outputs': {},
 'resources': [{'instances': [{'attributes': {'create_time': '2020-04-30T13:51:27.390Z',
                                              'display_name': 'sol22 - '
                                                              'ksjs726s',
                                              'id': 'folders/615899412414',
                                              'lifecycle_state': 'ACTIVE',
                                              'name': 'folders/615899412414',
                                              'parent': 'folders/943956663445',
                                              'timeouts': None},
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfX0=',
                               'schema_version': 0}],
                'mode': 'managed',
                'module': 'module.solution_folder',
                'name': 'solution_folder',
                'provider': 'provider.google',
                'type': 'google_folder'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-dev-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-dev-env',
                                              'number': '6570889872',
                                              'org_id': '',
                                              'project_id': 'sol22-dev-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.dev_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-prod-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-prod-env',
                                              'number': '1072288444773',
                                              'org_id': '',
                                              'project_id': 'sol22-prod-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.prod_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-staging-env-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-staging-env',
                                              'number': '292492613552',
                                              'org_id': '',
                                              'project_id': 'sol22-staging-env-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.staging_environment',
                'name': 'environment_project',
                'provider': 'provider.google',
                'type': 'google_project'},
               {'instances': [{'attributes': {'auto_create_network': True,
                                              'billing_account': None,
                                              'folder_id': '615899412414',
                                              'id': 'projects/sol22-workspace-ksjs726s',
                                              'labels': None,
                                              'name': 'sol22-workspace',
                                              'number': '555918489693',
                                              'org_id': '',
                                              'project_id': 'sol22-workspace-ksjs726s',
                                              'skip_delete': None,
                                              'timeouts': None},
                               'dependencies': ['module.solution_folder.google_folder.solution_folder'],
                               'private': 'eyJlMmJmYjczMC1lY2FhLTExZTYtOGY4OC0zNDM2M2JjN2M0YzAiOnsiY3JlYXRlIjoyNDAwMDAwMDAwMDAsImRlbGV0ZSI6MjQwMDAwMDAwMDAwLCJyZWFkIjoyNDAwMDAwMDAwMDAsInVwZGF0ZSI6MjQwMDAwMDAwMDAwfSwic2NoZW1hX3ZlcnNpb24iOiIxIn0=',
                               'schema_version': 1}],
                'mode': 'managed',
                'module': 'module.workspace_project',
                'name': 'workspace_project',
                'provider': 'provider.google',
                'type': 'google_project'}],
 'serial': 1,
 'terraform_version': '0.12.24',
 'version': 4}
my_json_s = str(json.dumps(my_json, separators=(',', ':')))


def next_taskid():
    task_cnt = next(counter)
    taskid = f"MOCKTASKID{task_cnt}"
    return taskid


def create(solutionDetails):
    retval = {
        "tf_return_code": 0,
        "status": "SUCCESS",
        "tf_state": my_json_s
    }
    return retval, 201


def delete(solutionDetails):
    retval = {
        "tf_return_code": 0,
        "status": "SUCCESS",
    }
    return retval, 200


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
        "tf_return_code": 0,
        "status": "SUCCESS",
        "tf_state": my_json_s
    }
    return retval, 201


def delete_solution_result(taskid):
    app.logger.info("DELETE SOLUTION RESULT %s",format(taskid))
    print(f"taskid: {taskid}")

    retval = {
        "tf_return_code": 0,
        "status": "SUCCESS",
        "tf_state": my_json_s
    }
    return retval, 200
