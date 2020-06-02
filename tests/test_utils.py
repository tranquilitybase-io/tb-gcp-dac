import unittest
from unittest import TestCase

from gcpdac.utils import labellize


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


if __name__ == '__main__':
    unittest.main()
