import json
import unittest

import requests

from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils
from src.test.python.tranquilitybase.gcpdac import local_test_runner


class ApplicationTest(unittest.TestCase):
    def test_create_application_async(self):
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/application_async/"
        request_json_file = local_test_runner.get_base_functional_test_path() \
                            + 'application/createApplication-input-example.json'
        FileUtils.file_exists(request_json_file)

        with open(request_json_file) as jsn:
            payload = json.load(jsn)
            data = json.dumps(payload, indent=4)

        response = requests.post(endpoint_url, data=data, headers=local_test_runner.headers)

        # TODO get valid json request to send
        self.assertEqual(201, response.status_code)

    def test_delete_application_async(self):
        taskid = 1
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/application_async/{taskid}"
        response = requests.delete(endpoint_url, headers=local_test_runner.headers)
        self.assertEqual(201, response.status_code)

    def test_create_application_async_result(self):
        taskid = 1
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/application_async/result/create/{taskid}"

        response = requests.get(endpoint_url, headers=local_test_runner.headers)
        self.assertEqual(200, response.status_code)

    def test_delete_application_async_result(self):
        taskid = 1
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/application_async/result/delete/{taskid}"
        response = requests.delete(endpoint_url, headers=local_test_runner.headers)
        self.assertEqual(405, response.status_code)


if __name__ == '__main__':
    unittest.main()
