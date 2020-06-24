import unittest
from unittest import TestCase

from gcpdac.utils import labellize, sanitize


class Utils_Test(TestCase):
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
