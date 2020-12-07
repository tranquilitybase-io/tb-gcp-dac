import unittest
import os
from unittest import TestCase

from main.python.tranquilitybase.gcpdac.configuration.envhelper import EnvHelper


class Utils_Test(TestCase):

    def test_config(self):
        os.environ["APP_PORT"] = "200"
        environment_helper = EnvHelper(False)
        environment_helper.get_app_port()

        env_start = "200"
        env_end = os.environ["APP_PORT"]
        self.assertEqual(env_start, env_end)


if __name__ == '__main__':
    unittest.main()
