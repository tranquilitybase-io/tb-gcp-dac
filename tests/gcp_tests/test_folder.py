import unittest
from time import sleep
from celery import states
from tests.gcp_tests.folder_utils import create_folder_task, delete_folder_task, create_folder_task_result, \
    delete_folder_task_result

validParentFolderId = "940168182397"
validFolderName = "TEST_FOLDER"

class FolderTest(unittest.TestCase):
    def test_folder(self):

        print("Creating a folder")

        taskid = create_folder_task(validFolderName, validParentFolderId)
        print("Celery task id {}".format(taskid))
        status = ''
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = create_folder_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)

        self.assertEqual(states.SUCCESS, status)

        print("Deleting a folder")
        taskid = delete_folder_task(validFolderName)
        print("Celery task id {}".format(taskid))
        status = ''
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = delete_folder_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)

        self.assertEqual(states.SUCCESS, status)


if __name__ == '__main__':
    unittest.main()
