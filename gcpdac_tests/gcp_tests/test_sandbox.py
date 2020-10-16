import json
import unittest
from time import sleep

from celery import states

from gcpdac_tests.gcp_tests import config
from gcpdac_tests.gcp_tests.sandbox_utils import create_sandbox_task, create_sandbox_task_result, delete_sandbox_task, \
    delete_sandbox_task_result

sandbox_id = 1001
team_id = 1001
business_unit = 'BU-1'
cost_code = 'CC-1'
deployment_folder_id = config.base_folder_id
sandbox_name = 'sandboxone'
sandbox_description = 'sandbox one description'
teamCloudIdentityGroup = config.teamCloudIdentityGroup
team_name = 'dev team'
created_by = 'jnsh'
sandbox_json = {
    'businessUnit': business_unit,
    'costCode': cost_code,
    'createdBy': created_by,
    'deploymentFolderId': deployment_folder_id,
    'description': sandbox_description,
    'id': sandbox_id,
    'name': sandbox_name,
    'teamCloudIdentityGroup': teamCloudIdentityGroup,
    'teamId': team_id,
    'teamName': team_name
}


def get_payload():
    return sandbox_json


def get_sandboxId():
    return sandbox_id


class sandboxTest(unittest.TestCase):
    def test_sandbox(self):
        sandbox_payload = self.create_sandbox(get_payload())

        self.delete_sandbox()

        # check sandbox values after deleting sandbox
        self.check_values(sandbox_response=json.loads(sandbox_payload), sandbox_input=get_payload())

    def delete_sandbox(self):
        taskid = delete_sandbox_task(get_sandboxId())
        print("Deleting a sandbox")
        print("Celery task id {}".format(taskid))
        status = ''
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = delete_sandbox_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)

    def create_sandbox(self, sandbox_input):
        taskid = create_sandbox_task(sandbox_input)
        print("Creating a sandbox")
        print("Celery task id {}".format(taskid))
        status = ''
        payload = {}
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = create_sandbox_task_result(taskid)
            print('Status {}'.format(status))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)
        print('Payload {}'.format(payload))
        return payload

    def check_values(self, sandbox_response, sandbox_input):
        self.assertFalse("billing_account_id" in sandbox_response)

        sandbox_project = sandbox_response["sandbox_project"]["value"]

        self.check_common_project_labels(sandbox_project["labels"])

        sandbox_folder = sandbox_response["sandbox_folder"]["value"]
        display_name = sandbox_folder["display_name"]

    def check_common_project_labels(self, labels):
        if 'cost-code' not in labels:
            self.fail("No cost-code label")
        if 'business-unit' not in labels:
            self.fail("No business-unit label")
        if 'team' not in labels:
            self.fail("No team label")
        if 'created-by' not in labels:
            self.fail("No created-by label")
        if 'environment' not in labels:
            self.fail("No environment label")


if __name__ == '__main__':
    unittest.main()
