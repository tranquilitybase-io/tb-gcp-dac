import unittest
from unittest import TestCase

from src.main.python.tranquilitybase.gcpdac.main.core.onboarding import clone_repo_locally, cleanup


class UtilsTest(TestCase):

    def test_onboarding(self):
        clone_repo_locally("https://github.com/tranquilitybase-io/tb-activator-gft-base")
        cleanup()


if __name__ == '__main__':
    unittest.main()