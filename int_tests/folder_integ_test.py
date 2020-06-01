from time import sleep

from int_tests.folder_utils import create_folder_task, delete_folder_task, create_folder_task_result, \
    delete_folder_task_result

validParentFolderId = "940168182397"
validFolderName = "TEST_FOLDER"

taskid=create_folder_task(validFolderName, validParentFolderId)
print(taskid)
status = ''
while (status != 'SUCCESS' and status != 'FAILURE'):
    status, payload = create_folder_task_result(taskid)
    print('Status {}'.format(status))
    print('Payload {}'.format(payload))
    sleep(10)

taskid=delete_folder_task(validFolderName)
print(taskid)
status = ''
while (status != 'SUCCESS' and status != 'FAILURE'):
    status, payload = delete_folder_task_result(taskid)
    print('Status {}'.format(status))
    print('Payload {}'.format(payload))
    sleep(10)
