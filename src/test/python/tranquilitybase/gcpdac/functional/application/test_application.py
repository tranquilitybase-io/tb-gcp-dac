import json
import os
import unittest
import requests

from src.test.python.tranquilitybase.gcpdac import local_test_runner


class ApplicationTest(unittest.TestCase):
    def test_application(self):
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/application_async/"

        print(os.getcwd())

        with open('functional/application/createApplication-input-example.json') as jsn:
            payload = json.load(jsn)
            data = json.dumps(payload, indent=4)

        response = requests.post(endpoint_url, data=data, headers=local_test_runner.headers)
        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()
