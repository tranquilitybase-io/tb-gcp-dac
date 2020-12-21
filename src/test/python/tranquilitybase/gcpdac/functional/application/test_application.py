import json
import unittest

import requests

from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils
from src.test.python.tranquilitybase.gcpdac import local_test_runner


class ApplicationTest(unittest.TestCase):
    def test_application(self):
        pass
        # endpoint_url = f"http://{local_test_runner.houston_url()}/dac/application_async/"
        # request_json_file = local_test_runner.get_base_functional_test_path() \
        #                     + 'application/createApplication-input-example.json'
        # FileUtils.file_exists(request_json_file)
        #
        # with open(request_json_file) as jsn:
        #     payload = json.load(jsn)
        #     data = json.dumps(payload, indent=4)
        #
        # response = requests.post(endpoint_url, data=data, headers=local_test_runner.headers)
        # self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
