import unittest
import requests
from celery import states

HOUSTON_SERVICE_URL = "0.0.0.0"
headers = {"Content-Type": "application/json"}


class ApplicationTest(unittest.TestCase):
    def test_application(self):
        endpoint_url = f"http://{HOUSTON_SERVICE_URL}/api/health/"
        response = requests.get(endpoint_url, headers=headers)
        self.assertEqual(states.SUCCESS, response)


if __name__ == '__main__':
    unittest.main()
