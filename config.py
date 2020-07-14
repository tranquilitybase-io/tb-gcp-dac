import os
import connexion
import yaml
from flask_marshmallow import Marshmallow

from gcpdac.local_logging import get_logger
from gcpdac.utils import setDefaultGoogleCloudProject, make_celery

logger = get_logger('tb-gcp-dac')
logger.info("Logger initialised")

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
DEFAULT_SHELL = "/bin/bash"
JENKINS_BASE_URL = os.environ['JENKINS_BASE_URL']

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

app.config.update(
    CELERY_BROKER_URL=os.environ['CELERY_RESULT_BACKEND'],
    CELERY_RESULT_BACKEND=os.environ['CELERY_BROKER_URL'],
)

ma = Marshmallow(app)

setDefaultGoogleCloudProject()

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
