
HOUSTON_SERVICE_URL = "0.0.0.0:3100"
headers = {"Content-Type": "application/json"}


def houston_url():
    return HOUSTON_SERVICE_URL


import unittest
loader = unittest.TestLoader()

import os
for entry in os.scandir('.'):
    print(entry.name)


if __name__ == '__main__':
    start_dir = 'unit'
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite)

    start_dir = 'functional.application'
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner()
    runner.run(suite)