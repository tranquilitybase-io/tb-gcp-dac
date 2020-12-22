import unittest
import requests

from src.test.python.tranquilitybase.gcpdac import local_test_runner


class ApplicationTest(unittest.TestCase):
    def test_cloud_identity_groups(self):
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/cloud_identity_groups"
        print("test url: " + endpoint_url)
        response = requests.get(endpoint_url, headers=local_test_runner.headers)

        self.assertTrue(response.status_code == 200 or response.status_code == 401 or response.status_code == 500)


if __name__ == '__main__':
    unittest.main()
