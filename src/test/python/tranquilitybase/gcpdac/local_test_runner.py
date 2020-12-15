import unittest
from unittest import TestSuite

HOUSTON_SERVICE_URL = "0.0.0.0:3100"
headers = {"Content-Type": "application/json"}


def houston_url():
    return HOUSTON_SERVICE_URL


def load_tests(loader, tests, pattern):
    ''' Discover and load all unit tests in all files named ``*_test.py`` in ``./src/``
    '''
    suite = TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('.', pattern='test_*'):
        for test_suite in all_test_suite:
            suite.addTests(test_suite)

    return suite


if __name__ == '__main__':
    unittest.main()