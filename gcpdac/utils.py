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
    # TODO rules for a label are different then for projects and other resources. Need to define different checks for different resources
    return sanitize(labelText)


# This method should 'sanitize' a given name for GCP usage
# Does the following:
# Makes alphabetic characters lower case
# Replaces anything other alphanumeric/hyphen with hyphen
# first and last characters alphabetic
# name < 63 chars
def sanitize(name):
    # make lower case and replace characters other than alphanumeric and hyphen
    valid = False
    while valid == False:
        name = name.lower()
        name = name[0:63]
        name = re.sub('[^0-9a-z-]+', '-', name)
        if not re.search('[a-zA-Z]', name):
            name = 'a{}a'.format(name)
        if name[0].isnumeric() or name[0] == '-':
            name = name[1:]
        if name[-1].isnumeric() or name[-1] == '-':
            name = name[:-1]
        valid = True

    return name


def remove_keys_from_dict(payload, keys_to_remove):
    for key in keys_to_remove:
        with suppress(KeyError):
            del payload[key]

    return payload
