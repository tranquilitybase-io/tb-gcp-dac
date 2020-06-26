import json
import unittest
from time import sleep

from celery import states

from tests.gcp_tests.activator_utils import delete_activator_task, delete_activator_task_result, create_activator_task, \
    create_activator_task_result

activator_id = 101
solution_id = 1001
# activator_git_url = "https://github.com/tranquilitybase-io/tb-activator-gft-base.git"
activator_git_url = "https://source.developers.google.com/p/workspace-93b7sc-ksjs726s/r/activator-testapp"
# TODO write test that creates solution first, retrieves workspace project then deploys activator
# workspaceProjectId = "workspace-j8u3pn-ksjs726s"
workspaceProjectId = None
activator_name = "testapp"

activator_json = {
    "id": activator_id,
    "name": activator_name,
    "description": "Test app",
    "solutionId": solution_id,
    "workspaceProjectId": workspaceProjectId,
    "activatorGitUrl": activator_git_url
}


def get_payload():
    return activator_json


def get_activatorId():
    return activator_id


class ActivatorTest(unittest.TestCase):
    # @unittest.skip("TODO Test needs more setup before running")
    def test_activator(self):
        if workspaceProjectId == None:
            self.fail("Set a valid solution workspace project id to test")
        response = self.deploy_activator(get_payload())
        response = json.loads(response)

        self.assertEqual("activator-testapp", response["repo_name"])

    def deploy_activator(self, activator_input):
        taskid = create_activator_task(activator_input)
        print("Creating a activator")
        print("Celery task id {}".format(taskid))
        status = ''
        payload = {}
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = create_activator_task_result(taskid)
            print('Status {}'.format(status))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)
        print('Payload {}'.format(payload))
        return payload

    def delete_activator(self):
        taskid = delete_activator_task(get_activatorId())
        print("Deleting a activator")
        print("Celery task id {}".format(taskid))
        status = ''
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = delete_activator_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)


if __name__ == '__main__':
    unittest.main()
