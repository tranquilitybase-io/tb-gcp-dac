import unittest

import requests

headers = {'Content-Type': 'application/json'}


def get_metadata():
    url = 'http://localhost:3100/api/metadata'
    return requests.get(url, headers=headers)


class MetadataTest(unittest.TestCase):
    def test_metadata(self):
        print("Get Metadata")

        response = get_metadata()
        resp_json = response.json()
        root_folder_id = resp_json['root_folder_id']
        self.assertEqual(200, response.status_code)
        self.assertTrue(int(root_folder_id) > 0)


if __name__ == '__main__':
    unittest.main()
