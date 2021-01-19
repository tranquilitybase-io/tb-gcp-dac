import os
import unittest
from unittest import TestSuite

from src.main.python.tranquilitybase.gcpdac.configuration.helpers.envhelper import EnvHelper

global HOUSTON_SERVICE_URL
HOUSTON_SERVICE_URL = None
headers = {"Content-Type": "application/json"}


def establish_hostname():
    hostname = "0.0.0.0"
    port = "3100"

    if os.getenv('TEST_TARGET_HOSTNAME'):
        hostname = os.environ['TEST_TARGET_HOSTNAME']

    if os.getenv('TEST_TARGET_PORT'):
        port = os.environ['TEST_TARGET_PORT']

    global HOUSTON_SERVICE_URL
    HOUSTON_SERVICE_URL = hostname + ":" + port
    HOUSTON_SERVICE_URL = HOUSTON_SERVICE_URL + "/dac"


def get_base_functional_test_path():
    root = "/app"
    if EnvHelper.is_ide():
        root = "../../../../../"

    return root + "/src/test/python/tranquilitybase/gcpdac/functional/"


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

