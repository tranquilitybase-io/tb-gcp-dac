import json
import unittest
from time import sleep

from celery import states

from tests.gcp_tests.solution_utils import create_solution_task, create_solution_task_result, delete_solution_task, \
    delete_solution_task_result

solution_id = 1001
business_unit = 'BU-1'
cost_centre = 'CC-1'
deployment_folder_id = '940168182397'
environments = [
    'Development',
    'QA',
    'Staging',
    'Production'
]
solution_json = {
    'id': solution_id,
    'name': 'solutionone',
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
    'teams': 1,
    'lastUpdated': '2020-04-21T08:30:52+00:00'
}


def get_payload():
    return solution_json


def get_solutionId():
    return solution_id


class SolutionTest(unittest.TestCase):
    def test_solution(self):
        taskid = create_solution_task(get_payload())
        print("Creating a solution")
        print("Celery task id {}".format(taskid))
        status = ''
        payload = {}
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = create_solution_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)

        self.assertEqual(states.SUCCESS, status)

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

        # check solution values after deleting solution
        self.check_values(solution=json.loads(payload))


    def check_values(self, solution):
        print(solution)
        environment_projects = solution["environment_projects"]
        print(environment_projects)
        for environment in json.loads(environment_projects):
            environment_label = environment["value"]["labels"]["environment"]
            self.assertTrue(environment_label in environments)
        workspace_project = solution["workspace_project"]
        solution_folder = solution["solution_folder"]
        # self.assertEqual(created_folder_name, display_name)
        # self.assertEqual(parent_folder_id, return_parent_folder_id.replace("folders/", ""))
        # self.assertTrue(int(folder_id.replace("folders/", "")) > 0)

# {
#     "environment_projects": {
#         "sensitive": false,
#         "type": [
#             "tuple",
#             [
#                 [
#                     "object",
#                     {
#                         "auto_create_network": "bool",
#                         "billing_account": "string",
#                         "folder_id": "string",
#                         "id": "string",
#                         "labels": [
#                             "map",
#                             "string"
#                         ],
#                         "name": "string",
#                         "number": "string",
#                         "org_id": "string",
#                         "project_id": "string",
#                         "skip_delete": "bool",
#                         "timeouts": [
#                             "object",
#                             {
#                                 "create": "string",
#                                 "delete": "string",
#                                 "read": "string",
#                                 "update": "string"
#                             }
#                         ]
#                     }
#                 ],
#                 [
#                     "object",
#                     {
#                         "auto_create_network": "bool",
#                         "billing_account": "string",
#                         "folder_id": "string",
#                         "id": "string",
#                         "labels": [
#                             "map",
#                             "string"
#                         ],
#                         "name": "string",
#                         "number": "string",
#                         "org_id": "string",
#                         "project_id": "string",
#                         "skip_delete": "bool",
#                         "timeouts": [
#                             "object",
#                             {
#                                 "create": "string",
#                                 "delete": "string",
#                                 "read": "string",
#                                 "update": "string"
#                             }
#                         ]
#                     }
#                 ],
#                 [
#                     "object",
#                     {
#                         "auto_create_network": "bool",
#                         "billing_account": "string",
#                         "folder_id": "string",
#                         "id": "string",
#                         "labels": [
#                             "map",
#                             "string"
#                         ],
#                         "name": "string",
#                         "number": "string",
#                         "org_id": "string",
#                         "project_id": "string",
#                         "skip_delete": "bool",
#                         "timeouts": [
#                             "object",
#                             {
#                                 "create": "string",
#                                 "delete": "string",
#                                 "read": "string",
#                                 "update": "string"
#                             }
#                         ]
#                     }
#                 ],
#                 [
#                     "object",
#                     {
#                         "auto_create_network": "bool",
#                         "billing_account": "string",
#                         "folder_id": "string",
#                         "id": "string",
#                         "labels": [
#                             "map",
#                             "string"
#                         ],
#                         "name": "string",
#                         "number": "string",
#                         "org_id": "string",
#                         "project_id": "string",
#                         "skip_delete": "bool",
#                         "timeouts": [
#                             "object",
#                             {
#                                 "create": "string",
#                                 "delete": "string",
#                                 "read": "string",
#                                 "update": "string"
#                             }
#                         ]
#                     }
#                 ]
#             ]
#         ],
#         "value": [
#             {
#                 "auto_create_network": true,
#                 "billing_account": "01A2F5-73127B-50AE5B",
#                 "folder_id": "626202176798",
#                 "id": "projects/development-dqo31l-ksjs726s",
#                 "labels": {
#                     "business_unit": "bu-1",
#                     "cost_centre": "cc-1",
#                     "environment": "development"
#                 },
#                 "name": "solutionone-development",
#                 "number": "51589750555",
#                 "org_id": "",
#                 "project_id": "development-dqo31l-ksjs726s",
#                 "skip_delete": null,
#                 "timeouts": null
#             },
#             {
#                 "auto_create_network": true,
#                 "billing_account": "01A2F5-73127B-50AE5B",
#                 "folder_id": "626202176798",
#                 "id": "projects/qa-dqo31l-ksjs726s",
#                 "labels": {
#                     "business_unit": "bu-1",
#                     "cost_centre": "cc-1",
#                     "environment": "qa"
#                 },
#                 "name": "solutionone-qa",
#                 "number": "852890918425",
#                 "org_id": "",
#                 "project_id": "qa-dqo31l-ksjs726s",
#                 "skip_delete": null,
#                 "timeouts": null
#             },
#             {
#                 "auto_create_network": true,
#                 "billing_account": "01A2F5-73127B-50AE5B",
#                 "folder_id": "626202176798",
#                 "id": "projects/staging-dqo31l-ksjs726s",
#                 "labels": {
#                     "business_unit": "bu-1",
#                     "cost_centre": "cc-1",
#                     "environment": "staging"
#                 },
#                 "name": "solutionone-staging",
#                 "number": "286756486039",
#                 "org_id": "",
#                 "project_id": "staging-dqo31l-ksjs726s",
#                 "skip_delete": null,
#                 "timeouts": null
#             },
#             {
#                 "auto_create_network": true,
#                 "billing_account": "01A2F5-73127B-50AE5B",
#                 "folder_id": "626202176798",
#                 "id": "projects/production-dqo31l-ksjs726s",
#                 "labels": {
#                     "business_unit": "bu-1",
#                     "cost_centre": "cc-1",
#                     "environment": "production"
#                 },
#                 "name": "solutionone-production",
#                 "number": "196262539761",
#                 "org_id": "",
#                 "project_id": "production-dqo31l-ksjs726s",
#                 "skip_delete": null,
#                 "timeouts": null
#             }
#         ]
#     },
#     "solution_folder": {
#         "sensitive": false,
#         "type": [
#             "object",
#             {
#                 "create_time": "string",
#                 "display_name": "string",
#                 "id": "string",
#                 "lifecycle_state": "string",
#                 "name": "string",
#                 "parent": "string",
#                 "timeouts": [
#                     "object",
#                     {
#                         "create": "string",
#                         "delete": "string",
#                         "read": "string",
#                         "update": "string"
#                     }
#                 ]
#             }
#         ],
#         "value": {
#             "create_time": "2020-06-02T14:39:24.106Z",
#             "display_name": "solutionone",
#             "id": "folders/626202176798",
#             "lifecycle_state": "ACTIVE",
#             "name": "folders/626202176798",
#             "parent": "folders/940168182397",
#             "timeouts": null
#         }
#     },
#     "workspace_project": {
#         "sensitive": false,
#         "type": [
#             "object",
#             {
#                 "auto_create_network": "bool",
#                 "billing_account": "string",
#                 "folder_id": "string",
#                 "id": "string",
#                 "labels": [
#                     "map",
#                     "string"
#                 ],
#                 "name": "string",
#                 "number": "string",
#                 "org_id": "string",
#                 "project_id": "string",
#                 "skip_delete": "bool",
#                 "timeouts": [
#                     "object",
#                     {
#                         "create": "string",
#                         "delete": "string",
#                         "read": "string",
#                         "update": "string"
#                     }
#                 ]
#             }
#         ],
#         "value": {
#             "auto_create_network": true,
#             "billing_account": "01A2F5-73127B-50AE5B",
#             "folder_id": "626202176798",
#             "id": "projects/workspace-dqo31l-ksjs726s",
#             "labels": {
#                 "business_unit": "bu-1",
#                 "cost_centre": "cc-1"
#             },
#             "name": "solutionone-workspace",
#             "number": "614177856418",
#             "org_id": "",
#             "project_id": "workspace-dqo31l-ksjs726s",
#             "skip_delete": null,
#             "timeouts": null
#         }
#     }
# }

if __name__ == '__main__':
    unittest.main()
