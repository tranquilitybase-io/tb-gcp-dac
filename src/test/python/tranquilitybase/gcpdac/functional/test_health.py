import unittest
import requests

from src.test.python.tranquilitybase.gcpdac import local_test_runner


class ApplicationTest(unittest.TestCase):
    def test_application(self):
        endpoint_url = f"http://{local_test_runner.houston_url()}/dac/health"
        print("test url: " + endpoint_url)
        response = requests.get(endpoint_url, headers=local_test_runner.headers)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
