import unittest
from time import sleep

from celery import states

from tests.gcp_tests.application_utils import delete_application_task, delete_application_task_result, \
    create_application_task, \
    create_application_task_result

application_id = 101
solution_id = 1001
# activator_git_url = "https://github.com/tranquilitybase-io/tb-activator-gft-base.git"
activator_git_url = "https://source.developers.google.com/p/workspace-93b7sc-ksjs726s/r/activator-testapp"
# TODO write test that creates solution first, retrieves workspace project then deploys activator
# workspaceProjectId = "workspace-j8u3pn-ksjs726s"
# deploymentProjectId = "development-j8u3pn-ksjs726s"
deploymentProjectId = None
workspaceProjectId = None
application_name = "testapp"
deploymentEnvironment = "DEV"

application_json = {
    "id": application_id,
    "name": application_name,
    "description": "Test app",
    "solutionId": solution_id,
    "workspaceProjectId": workspaceProjectId,
    "activatorGitUrl": activator_git_url,
    "deploymentEnvironment": deploymentEnvironment,
    "deploymentProjectId": deploymentProjectId,
    "mandatory_variables": {},
    "optional_variables": {}
}

application_json_incomplete = {
    "id": application_id,
    "name": application_name,
    "description": "Test app",
    "solutionId": solution_id
}


def get_payload():
    return application_json


def get_applicationId():
    return application_id


def deploy_application(application_input):
    taskid = create_application_task(application_input)
    print("Creating a application")
    print("Celery task id {}".format(taskid))
    status = ''
    payload = {}
    while (status != states.SUCCESS and status != states.FAILURE):
        print("Checking task {}".format(taskid))
        status, payload = create_application_task_result(taskid)
        print('Status {}'.format(status))
        sleep(10)
    return status, payload


class ApplicationTest(unittest.TestCase):
    # @unittest.skip("TODO Test needs more setup before running")
    def test_application(self):
        if workspaceProjectId == None:
            self.fail("Set a valid solution workspace project id to test")
        status, payload = deploy_application(application_json)
        # response = json.loads(response)
        self.assertEqual(states.SUCCESS, status)
        self.assertEqual("activator-testapp", payload["repo_name"])

    # TODO remove test when houston implements latest version of api
    def test_application_invalid_input(self):
        status, payload = deploy_application(application_json_incomplete)
        self.assertEqual(states.FAILURE, status)

        print("payload:{}".format(payload))

    def delete_application(self):
        taskid = delete_application_task(get_applicationId())
        print("Deleting a application")
        print("Celery task id {}".format(taskid))
        status = ''
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = delete_application_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)


if __name__ == '__main__':
    unittest.main()
