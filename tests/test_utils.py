import unittest
from unittest import TestCase

from gcpdac.utils import sanitize, labellize


class Utils_Test(TestCase):

    def test_labellize(self):
        # google label rules here - https://cloud.google.com/compute/docs/labeling-resources
        self.assertEqual("abc", labellize("abc"))
        self.assertEqual("ab-c", labellize("ab c"))
        self.assertEqual("ab-c", labellize("ab&c"))
        self.assertEqual("ab_c", labellize("ab_c"))
        self.assertEqual("ab-c", labellize("ab-c"))
        self.assertEqual("abc", labellize("ABC"))
        self.assertEqual("a123", labellize("123"))
        self.assertEqual("a-123", labellize("-123"))
        self.assertEqual("a-abc", labellize("-abc"))
        self.assertEqual("a_123", labellize("_123"))
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


if __name__ == '__main__':
    unittest.main()
