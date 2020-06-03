import unittest
from unittest import TestCase

from gcpdac.utils import labellize, remove_keys_from_dict


class Utils_Test(TestCase):
    def test_labellize(self):
        # google label rules here - https://cloud.google.com/compute/docs/labeling-resources
        self.assertEqual('abc', labellize('abc'))
        self.assertEqual('ab-c', labellize('ab c'))
        self.assertEqual('ab-c', labellize('ab&c'))
        self.assertEqual('ab_c', labellize('ab_c'))
        self.assertEqual('ab-c', labellize('ab-c'))
        self.assertEqual('abc', labellize('ABC'))
        self.assertEqual('a123', labellize('123'))
        self.assertEqual('a-123', labellize('-123'))
        self.assertEqual('a-abc', labellize('-abc'))
        self.assertEqual('a_123', labellize('_123'))
        self.assertEqual('abcdefghijklimnopqrstuvwxyz-0123456789_abcdefghijklimnopqrstuvw',
                         labellize('abcdefghijklimnopqrstuvwxyz-0123456789_abcdefghijklimnopqrstuvwxyz'))

    def test_remove_keys_from_dict(self):
        dictionary = {'abc': 123, 'def': {'abc': 567, 'ghi': 67, 'zzz': 78}, 'aaa': {'abc': {'xyz': 678}}}
        keys = ['abc', 'zzz']

        remove_keys_from_dict(dictionary, keys)
        self.assertEqual({'aaa': {}, 'def': {'ghi': 67}}, dictionary)

if __name__ == '__main__':
    unittest.main()
