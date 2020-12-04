import os


def consider_config():

    is_ide = os.getenv('IDE', default="false")

    if is_ide == "true":
        os.environ["DEBUG"] = "true"

        os.environ["DAC_JENKINS_USER"] = "DAC_JENKINS_USER"
        os.environ["DAC_JENKINS_PASSWORD"] = "DAC_JENKINS_PASSWORD"
        os.environ["JENKINS_BASE_URL"] = "JENKINS_BASE_URL"

        os.environ["CELERY_BROKER_URL"] = "CELERY_BROKER_URL"
        os.environ["CELERY_RESULT_BACKEND"] = "CELERY_RESULT_BACKEND"

        project_root = os.environ["PROJECT_ROOT"]
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = project_root + "/credentials/credentials.json"
        os.environ["GOOGLE_CLOUD_PROJECT"] = "test"

        os.environ["APP_PORT"] = "9999"


consider_config()


import logging


basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
import connexion
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

from src.main.python.tranquilitybase.gcpdac import config



logger = config.logger

connex_app = config.connex_app

gunicorn_logger = logging.getLogger("gunicorn.info")
connex_app.app.logger.handlers = gunicorn_logger.handlers
connex_app.app.logger.setLevel(gunicorn_logger.level)

connex_app.add_api('openapi.yml', strict_validation=True)

celery = config.get_celery()



if __name__ == "__main__":
    connex_app.run(port=os.environ['APP_PORT'], debug=os.environ['DEBUG'])
