from unittest import TestCase

from gcpdac.utils import labellize


class Test(TestCase):
    def test_labellize(self):
        assert labellize("abc") == "abc"
        assert labellize("ab c") == "ab-c"
        assert labellize("ab&c") == "ab-c"
        assert labellize("ab_c") == "ab_c"
        assert labellize("ab-c") == "ab-c"
        assert labellize("ABC") == "abc"
