import json
import unittest
from time import sleep
from celery import states
from tests.gcp_tests.folder_utils import create_folder_task, delete_folder_task, create_folder_task_result, \
    delete_folder_task_result

validParentFolderId = "940168182397"
validFolderName = "TEST_FOLDER"
longFolderName = "abcdefghijkl12345nopqrstuvwxyz"  # 31 chars


class FolderTest(unittest.TestCase):
    def test_folder(self):

        payload = self.create_folder(folder_name=validFolderName, parent_folder_id=validParentFolderId)
        folder = json.loads(payload)
        self.check_values(folder, created_folder_name=validFolderName, parent_folder_id=validParentFolderId)

        self.delete_folder(folder_name=validFolderName)

    def test_long_folder_name(self):
        payload = self.create_folder(folder_name=longFolderName, parent_folder_id=validParentFolderId)
        folder = json.loads(payload)
        self.check_values(folder, created_folder_name=longFolderName[0:30], parent_folder_id=validParentFolderId)

        self.delete_folder(folder_name=longFolderName)

    def check_values(self, folder, created_folder_name, parent_folder_id):
        display_name = folder["folder"]["value"]["display_name"]
        folder_id = folder["folder"]["value"]["id"]
        return_parent_folder_id = folder["folder"]["value"]["parent"]
        self.assertEqual(created_folder_name, display_name)
        self.assertEqual(parent_folder_id, return_parent_folder_id.replace("folders/", ""))
        self.assertTrue(int(folder_id.replace("folders/", "")) > 0)

    def delete_folder(self, folder_name):
        print("Deleting a folder")
        taskid = delete_folder_task(folder_name)
        print("Celery task id {}".format(taskid))
        status = ''
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = delete_folder_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)

    def create_folder(self, folder_name, parent_folder_id):
        print("Creating a folder")
        taskid = create_folder_task(folder_name, parent_folder_id)
        print("Celery task id {}".format(taskid))
        status = ''
        payload = {}
        while (status != states.SUCCESS and status != states.FAILURE):
            print("Checking task {}".format(taskid))
            status, payload = create_folder_task_result(taskid)
            print('Status {}'.format(status))
            print('Payload {}'.format(payload))
            sleep(10)
        self.assertEqual(states.SUCCESS, status)
        return payload


if __name__ == '__main__':
    unittest.main()
