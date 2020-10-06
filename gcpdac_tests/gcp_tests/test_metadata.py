import unittest

import requests
from gcpdac_tests.gcp_tests.common_utils import BASE_URL

headers = {'Content-Type': 'application/json'}


def get_metadata():
    url = '{}/metadata'.format(BASE_URL)
    return requests.get(url, headers=headers)


class MetadataTest(unittest.TestCase):
    def test_metadata(self):
        print("Get Metadata")

        response = get_metadata()
        resp_json = response.json()
        print(resp_json)
        root_folder_id = resp_json['root_folder_id']
        self.assertEqual(200, response.status_code)
        self.assertTrue(int(root_folder_id) > 0)


if __name__ == '__main__':
    unittest.main()
