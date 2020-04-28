import celery
import json
import os
import requests
from flask import abort
from pprint import pformat
from gcpdac.local_logging import get_logger
from gcpdac.solution_terraform import run_terraform
from flask import Flask

logger = get_logger()
logger.info("Logger initialised")

@celery.task()
def add_together():
    logger.info("ADD TOGETHER")
    return "ADD TOGETHER"
