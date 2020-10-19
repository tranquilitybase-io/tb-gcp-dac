from unittest import TestCase

from gcpdac.shell_utils import get_parent_folder_id, add_access_to_folders


class Test(TestCase):
    def test_get_parent_folder(self):
        folder_id = get_parent_folder_id(302197932093)
        self.assertTrue(folder_id != '')
        get_parent_folder_id(3045897349857932197932093)
        self.assertTrue(folder_id == '')

    def test_add_access(self):
        add_access_to_folders(302197932093, ["snul@gft.com"], 940089049397)
