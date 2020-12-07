import unittest
from unittest import TestCase

from main.python.tranquilitybase.lib.common.utils import labellize
from main.python.tranquilitybase.lib.common.utils import folderize
from main.python.tranquilitybase.lib.common.utils import sanitize


class Utils_Test(TestCase):

    def test_config(self):
        env = "JENKINS_BASE_URL"
        env2 = ""
        self.assertEqual(env, env2)


    def test_labellize(self):
        # google label rules here - https://cloud.google.com/compute/docs/labeling-resources
        self.assertEqual("abc", labellize("abc"))
        self.assertEqual("ab-c", labellize("ab c"))
        self.assertEqual("ab-c", labellize("ab&c"))
        self.assertEqual("ab_c", labellize("ab_c"))
        self.assertEqual("ab-c", labellize("ab-c"))
        self.assertEqual("abc", labellize("ABC"))
        self.assertEqual("123", labellize("123"))
        self.assertEqual("-123", labellize("-123"))
        self.assertEqual("abc-", labellize("abc-"))
        self.assertEqual("_123", labellize("_123"))
        self.assertEqual("èÿā", labellize("èÿā"))
        self.assertEqual("èÿāć", labellize("èÿāĆ"))
        self.assertEqual("abcdefghijklimnopqrstuvwxyz-0123456789_abcdefghijklimnopqrstuvw",
                         labellize("abcdefghijklimnopqrstuvwxyz-0123456789_abcdefghijklimnopqrstuvwxyz"))

    def test_sanitize(self):
        self.assertEqual("abc", sanitize("abc"))
        self.assertEqual("ab-c", sanitize("ab c"))
        self.assertEqual("ab-c", sanitize("ab&c"))
        self.assertEqual("ab-c", sanitize("ab_c"))
        self.assertEqual("ab-c", sanitize("ab-c"))
        self.assertEqual("abc", sanitize("ABC"))
        self.assertEqual("a123a", sanitize("123"))
        self.assertEqual("a-123a", sanitize("-123"))
        self.assertEqual("abc", sanitize("-abc"))
        self.assertEqual("a-123a", sanitize("_123"))
        self.assertEqual("abcdefghijklimnopqrstuvwxyz-0123456789-abcdefghijklimnopqrstuvw",
                         sanitize("abcdefghijklimnopqrstuvwxyz-0123456789-abcdefghijklimnopqrstuvwxyz"))

    def test_folderize(self):
        self.assertEqual("abc", folderize("abc"))
        self.assertEqual("ab-c", folderize("ab c"))
        self.assertEqual("ab-c", folderize("ab&c"))
        self.assertEqual("ab_c", folderize("ab_c"))
        self.assertEqual("ab-c", folderize("ab-c"))
        self.assertEqual("ABC", folderize("ABC"))
        self.assertEqual("123", folderize("123"))
        self.assertEqual("123", folderize("-123"))
        self.assertEqual("abc", folderize("-abc"))
        self.assertEqual("123", folderize("_123"))
        self.assertEqual("abcDEFghijklmnopqrstuvwxyz-012",
                         folderize("abcDEFghijklmnopqrstuvwxyz-0123456789-abcdefghijklimnopqrstuvwxyz"))


if __name__ == '__main__':
    unittest.main()
