import json
import unittest
import requests
from celery import states
from time import sleep

from unittest import TestCase
from src.test.python.tranquilitybase.gcpdac import local_test_runner
from tranquilitybase.gcpdac.integration.solution.solution_config import *


class UserFlowTests(unittest.TestCase):
    def test_solution(self):
        solutionTest_methods = SolutionTest_methods()
        solution_payload = solutionTest_methods.create_solution(get_payload())

        solutionTest_methods.delete_solution()

        # check solution values after deleting solution
        solutionTest_methods.check_values(solution_response=json.loads(solution_payload), solution_input=get_payload())


class SolutionTest_methods():

    def delete_solution(self):
        taskid = SolutionUtils.delete_solution_task()
        print("Deleting a solution")
        print("Celery task id {}".format(taskid))
        status = ''

        max_tries = 10
        try_count = 0
        while status != states.SUCCESS and status != states.FAILURE:
            try_count = try_count+1
            if try_count >= max_tries:
                break

            print("Checking task {}".format(taskid))
            status, payload = SolutionUtils.delete_solution_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)
        TestCase().assertEqual(states.SUCCESS, status)

    def create_solution(self, solution_input):
        taskid = SolutionUtils.create_solution_task(solution_input)
        print("Creating a solution")
        print("Celery task id {}".format(taskid))
        status = ''
        payload = {}

        max_tries = 10
        try_count = 0
        while status != states.SUCCESS and status != states.FAILURE:
            try_count = try_count+1
            if try_count >= max_tries:
                break

            print("Checking task {}".format(taskid))
            status, payload = SolutionUtils.create_solution_task_result(taskid)
            print('Status {}'.format(status))
            sleep(10)

        TestCase().assertEqual(states.SUCCESS, status)
        print('Payload {}'.format(payload))
        return payload

    def check_values(self, solution_response, solution_input):
        TestCase().assertFalse("billing_account_id" in solution_response)
        environment_projects = solution_response["environment_projects"]["value"]
        for environment_project in environment_projects:
            labels = environment_project["labels"]
            self.check_common_project_labels(labels)
            if 'environment' not in labels:
                TestCase().fail("No environment label")
            environment_label = labels['environment']
            if environment_label not in processed_environments:
                TestCase().fail("Invalid environment label")

        workspace_project = solution_response["workspace_project"]["value"]
        self.check_common_project_labels(workspace_project["labels"])

        solution_folder = solution_response["solution_folder"]["value"]
        display_name = solution_folder["display_name"]
        TestCase().assertEqual(solution_input['name'], display_name)

    def check_common_project_labels(self, labels):
        if 'cost-code' not in labels:
            TestCase().fail("No cost-code label")
        if 'business-unit' not in labels:
            TestCase().fail("No business-unit label")
        if 'team' not in labels:
            TestCase().fail("No team label")


class SolutionUtils:
    @staticmethod
    def create_solution_task(payload):
        endpoint_url = f"http://{local_test_runner.houston_url()}/solution_async/"

        data = json.dumps(payload, indent=4)
        resp = requests.post(endpoint_url, headers=local_test_runner.headers, data=data)

        resp_json = resp.json()
        task_id = resp_json['taskid']

        return task_id

    @staticmethod
    def create_solution_task_result(taskId):
        endpoint_url = f"http://{local_test_runner.houston_url()}/result/create/{taskId}"

        resp = requests.get(endpoint_url, headers=local_test_runner.headers)

        resp_json = resp.json()
        status = resp_json['status']
        payload = resp_json.get('payload', None)

        return status, payload

    @staticmethod
    def delete_solution_task(solutionId):
        url = '{}/solution_async/{}'.format(local_test_runner.houston_url(), solutionId)
        resp = requests.delete(url, headers=local_test_runner.headers)

        resp_json = resp.json()
        task_id = resp_json['taskid']

        return task_id

    @staticmethod
    def delete_solution_task_result(taskId):
        url = '{}/solution_async/result/delete/{}'.format(local_test_runner.houston_url(), taskId)
        resp = requests.get(url, headers=local_test_runner.headers)

        resp_json = resp.json()
        status = resp_json['status']
        payload = resp_json.get('payload', None)

        return status, payload