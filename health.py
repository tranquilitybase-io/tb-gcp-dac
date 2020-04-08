"""
Health check: Very basic health check, can extend in future
"""

# 3rd party modules
from flask import make_response, abort
from config import db, app
from pprint import pformat
import json
from extendedSchemas import HealthSchema


def check():
    """
    :return:       200
    """

    status = { "status": "Healthy" }

    schema = HealthSchema()
    data = schema.dump(status)
    return data
