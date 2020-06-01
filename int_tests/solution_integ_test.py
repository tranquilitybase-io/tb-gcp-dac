from time import sleep

from int_tests.solution_utils import create_solution_task, create_solution_task_result, delete_solution_task, \
    delete_solution_task_result

solutionId = 1001
payload = {
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

taskid = create_solution_task(payload)
print("Creating a solution")
print("Celery task id {}".format(taskid))
status = ''
while (status != 'SUCCESS' and status != 'FAILURE'):
    print("Checking task {}".format(taskid))
    status, payload = create_solution_task_result(taskid)
    print('Status {}'.format(status))
    print('Payload {}'.format(payload))
    sleep(10)

taskid = delete_solution_task(solutionId)
print("Deleting a solution")
print("Celery task id {}".format(taskid))
status = ''
while (status != 'SUCCESS' and status != 'FAILURE'):
    print("Checking task {}".format(taskid))
    status, payload = delete_solution_task_result(taskid)
    print('Status {}'.format(status))
    print('Payload {}'.format(payload))
    sleep(10)
