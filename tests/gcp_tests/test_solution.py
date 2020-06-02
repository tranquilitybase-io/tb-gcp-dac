import unittest
from time import sleep

from celery import states

from tests.gcp_tests.solution_utils import create_solution_task, create_solution_task_result, delete_solution_task, \
    delete_solution_task_result

solutionId = 1001
solution_json = {
    'id': solutionId,
    'name': 'solutionone',
    'description': 'solution one description',
    'businessUnit': 'BU-1',
    'costCentre': 'CC-1',
    'ci': 'jenkins',
    'cd': 'jenkins',
    'sourceControl': 'git',
    'deploymentFolderId': '940168182397',
    'environments': [
        'Development',
        'QA',
        'Staging',
        'Production'
    ],
    'active': True,
    'favourite': True,
    'teams': 1,
    'lastUpdated': '2020-04-21T08:30:52+00:00'
}


def get_payload():
    return solution_json

def get_solutionId():
    return solutionId


class SolutionTest(unittest.TestCase):
    def test_solution(self):
        taskid = create_solution_task(get_payload())
        print("Creating a solution")
        print("Celery task id {}".format(taskid))
        status = ''
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


if __name__ == '__main__':
    unittest.main()
