import os
import random
import re
import string
from contextlib import suppress

import yaml
from celery import Celery
from google.cloud import storage

import celeryconfig


def setDefaultGoogleCloudProject():
    with open('/app/ec-config.yaml') as f:
        try:
            data: dict = yaml.safe_load(f)
            GOOGLE_CLOUD_PROJECT = data.get("ec_project_name")
            if not GOOGLE_CLOUD_PROJECT:
                raise ValueError("No GOOGLE_CLOUD_PROJECT set for Flask application")
            print(data)
        except yaml.YAMLError as exc:
            raise SystemError("Failed to parse EC YAML after successfully opening - {}".format(exc))
    print("GOOGLE_CLOUD_PROJECT: {}".format(GOOGLE_CLOUD_PROJECT))
    storage.Client(project=GOOGLE_CLOUD_PROJECT)


def make_celery(name):
    celery = Celery(
        name,
        backend=os.environ['CELERY_RESULT_BACKEND'],
        broker=os.environ['CELERY_BROKER_URL'],
        config_source=celeryconfig

    )

    return celery


def random_element(num_chars):
    """
    generates a random string of numbers and lower case letters
    :type num_chars: int
    """
    characters: str = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for i in range(num_chars))


def labellize(labelText):
    # make text valid for a Google Cloud label
    # label rules here - https://cloud.google.com/compute/docs/labeling-resources
    # in summary - lower case characters, numbers, dash or hyphen. <= 63 characters
    labelText = sanitize(labelText)
    firstChar = labelText[0]
    if firstChar.isnumeric() or firstChar == '-' or firstChar == '_':
        labelText = "a" + labelText
    if len(labelText) > 63:
        labelText = labelText[0:63]
    return labelText


def sanitize(x):
    # make lower case and replace characters other than alphanumeric, - and _
    x = x.lower()
    x = re.sub('[^0-9a-z-_]+', '-', x)
    return x


def remove_keys_from_dict(payload, keys_to_remove):
    for key in keys_to_remove:
        with suppress(KeyError):
            del payload[key]

    return payload

def read_config_map():
    # Returns the EC configuration as a dictionary

    try:
        with open("/app/ec-config.yaml", 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.exception("Failed to parse EC YAML after successfully opening - {}".format(exc))
                raise
    except Exception:
        logger.exception("Failed to load EC YAML file")
        raise

