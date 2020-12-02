import json
import os.path
from unittest import *

from gcloud import resource_manager
from mockito import *


class Test(TestCase):

    def test_get_ec_config(self):
        when(os.path).not_exists('/app/ec-config.yaml').thenReturn(self.fail("ec-config.yaml doesn't exist"))

    def test_get_destination_project(self):
        rm = mock(resource_manager.Client())
        proj_list = rm.list_projects()
        when(proj_list is None).thenReturn(self.fail("Empty projects list"))

    def test_get_repo_uri(self):
        json_data = mock(
            json.loads('{"activatorName": "tb-gcp-hpc-activator", "repoURL":"someurl", "tagName": "sometag"}'))
        when(json_data).self.assertNotEqual(json_data, {"key1": "value1"}).thenReturn(
            self.fail("Failed to return valid return url"))
