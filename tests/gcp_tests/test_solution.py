import json
import unittest
from time import sleep

from celery import states

from gcpdac.utils import labellize
from tests.gcp_tests import config
from tests.gcp_tests.solution_utils import create_solution_task, create_solution_task_result, delete_solution_task, \
    delete_solution_task_result

solution_id = 1001
business_unit = 'BU-1'
cost_centre = 'CC-1'
deployment_folder_id = config.base_folder_id
team_members = config.team_members
environments = [
    {'name':'Development',
     'id': 1,
     'sharedVPCProjectId': 'dummy'
     },
    {'name':'QA',
     'id': 2,
     'sharedVPCProjectId': 'dummy'
     },
    {'name':'Staging',
     'id': 3,
     'sharedVPCProjectId': 'dummy'
     },
    {'name':'Production',
     'id': 4,
     'sharedVPCProjectId': 'dummy'
     }
]
environment_names = map(lambda x : x['name'], environments)
processed_environments = map(labellize, environment_names)
solution_name = 'solutionone'
solution_json = {
    'id': solution_id,
    'name': solution_name,
    'description': 'solution one description',
    'businessUnit': business_unit,
    'costCentre': cost_centre,
    'ci': 'jenkins',
    'cd': 'jenkins',
    'sourceControl': 'git',
    'deploymentFolderId': deployment_folder_id,
    'environments': environments,
    'active': True,
    'favourite': True,
    "teamId": 1,
    "team": {
        "lastUpdated": "2020-03-01 12:34:56",
        "businessUnitId": 1,
        "teamMembers": team_members,
        "businessUnit": {
            "name": "Modern Apps",
            "isActive": True,
            "id": 1,
            "description": "Modern Apps"
        },
        "isActive": True,
        "id": 1,
        "description": "All Developers",
        "name": "Developers"
    },
    'lastUpdated': '2020-04-21T08:30:52+00:00'
}


def get_payload():
    return solution_json


def get_solutionId():
    return solution_id


class SolutionTest(unittest.TestCase):
    def test_solution(self):
        solution_payload = self.create_solution(get_payload())

        self.delete_solution()

        # check solution values after deleting solution
        self.check_values(solution_response=json.loads(solution_payload), solution_input=get_payload())

    def delete_solution(self):
        taskid = delete_solution_task(get_solutionId())
        print("Deleting a solution")
        print("Celery task id {}".format(taskid))
        status = ''
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = delete_solution_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)

    def create_solution(self, solution_input):
        taskid = create_solution_task(solution_input)
        print("Creating a solution")
        print("Celery task id {}".format(taskid))
        status = ''
        payload = {}
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = create_solution_task_result(taskid)
            print('Status {}'.format(status))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)
        print('Payload {}'.format(payload))
        return payload

    def check_values(self, solution_response, solution_input):
        self.assertFalse("billing_account_id" in solution_response)
        environment_projects = solution_response["environment_projects"]["value"]
        for environment_project in environment_projects:
            labels = environment_project["labels"]
            self.check_common_project_labels(labels)
            if 'environment' not in labels:
                self.fail("No environment label")
            environment_label = labels['environment']
            if environment_label not in processed_environments:
                self.fail("Invalid environment label")

        workspace_project = solution_response["workspace_project"]["value"]
        self.check_common_project_labels(workspace_project["labels"])

        solution_folder = solution_response["solution_folder"]["value"]
        display_name = solution_folder["display_name"]
        self.assertEqual(solution_input['name'], display_name)

    def check_common_project_labels(self, labels):
        if 'cost_centre' not in labels:
            self.fail("No cost_centre label")
        if 'business_unit' not in labels:
            self.fail("No business_unit label")
        if 'team' not in labels:
            self.fail("No team label")


if __name__ == '__main__':
    unittest.main()
