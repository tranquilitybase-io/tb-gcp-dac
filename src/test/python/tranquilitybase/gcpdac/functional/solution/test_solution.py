import json
import os
import unittest
import requests

from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils
from src.test.python.tranquilitybase.gcpdac import local_test_runner


class SolutionTest(unittest.TestCase):
    def test_application(self):
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/solution_async/"

        request_json_file = local_test_runner.get_base_functional_test_path() \
                            + 'application/createSolution-input-example.json'
        FileUtils.file_exists(request_json_file)

        # print(os.getcwd())
        #
        # with open('functional/solution/createSolution-input-example.json') as jsn:
        #     payload = json.load(jsn)
        #     data = json.dumps(payload, indent=4)
        #
        # response = requests.post(endpoint_url, data=data, headers=local_test_runner.headers)
        # self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()