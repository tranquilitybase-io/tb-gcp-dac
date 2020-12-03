import os

import connexion
import yaml
from celery import Celery
from flask_marshmallow import Marshmallow
from google.cloud import storage
from pathlib import Path
from src.main.python.tranquilitybase.gcpdac.celery import celeryconfig
from src.main.python.tranquilitybase.gcpdac.core.exceptions import DacJenkinsError

from src.main.python.tranquilitybase.lib.common.local_logging import get_logger


logger = get_logger('tb-gcp-dac')
logger.info("Logger initialised")

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
DEFAULT_SHELL = "/bin/bash"

def setJenkinsBaseUrl():
    try:
        jenkins_base_url = "http://" + os.environ['JENKINS_BASE_URL']
    except Exception as e:
        print(e)
        raise DacJenkinsError(
            "Jenkins environment variables not set. Check JENKINS_BASE_URL are set")
    return jenkins_base_url

JENKINS_BASE_URL = setJenkinsBaseUrl()
JENKINS_USER = os.environ['DAC_JENKINS_USER']
JENKINS_PASSWORD = os.environ['DAC_JENKINS_PASSWORD']

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

app.config.update(
    CELERY_BROKER_URL=os.environ['CELERY_BROKER_URL'],
    CELERY_RESULT_BACKEND=os.environ['CELERY_RESULT_BACKEND'],
)

ma = Marshmallow(app)


def setDefaultGoogleCloudProject():
    file_path = basedir + "/" + "ec-config.yaml"
    print("file_path " + str(file_path))
    file = Path(file_path)
    if not file.is_file():
        raise Exception("No file found for " + file_path)

    with open(file_path) as f:
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


setDefaultGoogleCloudProject()


def make_celery(name):
    celery = Celery(
        name,
        backend=os.environ['CELERY_RESULT_BACKEND'],
        broker=os.environ['CELERY_BROKER_URL'],
        config_source=celeryconfig
    )

    return celery


celery_app = make_celery(__name__)


def get_celery():
    return celery_app


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


ec_config = read_config_map()
