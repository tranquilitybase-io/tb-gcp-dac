import os
import unittest
from unittest import TestSuite

global HOUSTON_SERVICE_URL
HOUSTON_SERVICE_URL = None
headers = {"Content-Type": "application/json"}


def establish_hostname():
    hostname = "0.0.0.0"
    port = "3100"

    if os.getenv('DOCKER_HOSTNAME'):
        hostname = os.environ['DOCKER_HOSTNAME']

    if os.getenv('APP_PORT'):
        port = os.environ['APP_PORT']

    global HOUSTON_SERVICE_URL
    HOUSTON_SERVICE_URL = hostname + ":" + port


def houston_url():
    global HOUSTON_SERVICE_URL
    return HOUSTON_SERVICE_URL


def load_tests(loader, tests, pattern):
    ''' Discover and load all unit tests
    '''

    suite = TestSuite()
    for all_test_suite in unittest.defaultTestLoader.discover('.', pattern='test_*'):
        for test_suite in all_test_suite:
            suite.addTests(test_suite)

    return suite


establish_hostname()
if __name__ == '__main__':
    unittest.main()