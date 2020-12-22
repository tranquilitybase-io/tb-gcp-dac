import unittest
import requests

from src.test.python.tranquilitybase.gcpdac import local_test_runner


class ApplicationTest(unittest.TestCase):
    def test_metadata(self):
        endpoint_url = f"http://{local_test_runner.houston_url()}/metadata"
        print("test url: " + endpoint_url)
        response = requests.get(endpoint_url, headers=local_test_runner.headers)
        self.assertEqual(200, response.status_code)

        resp_json = response.json()
        print(resp_json)
        root_folder_id = resp_json['root_folder_id']
        self.assertTrue(root_folder_id == "WILL BE NEEDED NOT NOW")
        # self.assertTrue(int(root_folder_id) > 0)


if __name__ == '__main__':
    unittest.main()
