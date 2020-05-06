import os
import re

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


def labellize(labelText):
    # make text valid for a Google Cloud label
    # label rules here - https://cloud.google.com/compute/docs/labeling-resources
    # in summary - lower case characters, numbers, dash or hyphen. <= 63 characters
    labelText = labelText.lower()
    labelText = re.sub('[^0-9a-z-_]+', '-', labelText)
    firstChar = labelText[0]
    if firstChar.isnumeric() or firstChar == '-' or firstChar == '_':
        labelText = "a" + labelText
    if len(labelText) > 63:
        labelText = labelText[0:63]
    return labelText
