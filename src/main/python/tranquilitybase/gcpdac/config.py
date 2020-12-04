import os

import connexion
from celery import Celery
from flask_marshmallow import Marshmallow
from google.cloud import storage
from src.main.python.tranquilitybase.gcpdac.celery import celeryconfig

from src.main.python.tranquilitybase.lib.common.local_logging import get_logger
from src.main.python.tranquilitybase.gcpdac.configuration.confighelper import ConfigHelper
from src.main.python.tranquilitybase.gcpdac.configuration.jenkinshelper import JenkinsHelper


# ---- Logging -----
logger = get_logger('tb-gcp-dac')
logger.info("Logger initialised")


# ---- Jenkins -----
jenkinsHelper = JenkinsHelper()
JENKINS_BASE_URL = jenkinsHelper.jenkins_base_url
JENKINS_USER = jenkinsHelper.jenkins_user
JENKINS_PASSWORD = jenkinsHelper.jenkins_password


# ----- Config ----
configHelper = ConfigHelper()
ec_config = ConfigHelper.read_config_map()
configHelper.get_gcp_project_name()
print("GOOGLE_CLOUD_PROJECT: {}".format(configHelper.get_gcp_project_name()))
storage.Client(project=configHelper.get_gcp_project_name())


# ---- Shell -----
DEFAULT_SHELL = "/bin/bash"


# ---- connexion -----
basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

app.config.update(
    CELERY_BROKER_URL=os.environ['CELERY_BROKER_URL'],
    CELERY_RESULT_BACKEND=os.environ['CELERY_RESULT_BACKEND'],
)


# ---- Marshmallow/Flask -----
ma = Marshmallow(app)


# ---- Celery -----
def make_celery(name):
    celery = Celery(
        name,
        backend=os.environ['CELERY_RESULT_BACKEND'],
        broker=os.environ['CELERY_BROKER_URL'],
        config_source=celeryconfig
    )

    return celery


def get_celery():
    return celery_app


celery_app = make_celery(__name__)
