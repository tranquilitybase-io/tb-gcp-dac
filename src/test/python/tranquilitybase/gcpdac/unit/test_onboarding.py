import unittest
from unittest import TestCase

from src.main.python.tranquilitybase.gcpdac.main.core.onboarding import clone_repo_locally


class UtilsTest(TestCase):

    def test_clone_repo_multiple_calls(self):
        clone_repo_locally("https://github.com/tranquilitybase-io/tb-activator-gft-base")
        clone_repo_locally("https://github.com/tranquilitybase-io/tb-activator-gft-base")


if __name__ == '__main__':
    unittest.main()
