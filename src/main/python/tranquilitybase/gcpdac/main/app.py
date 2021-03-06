import os
import connexion

from flask_marshmallow import Marshmallow

from src.main.python.tranquilitybase.gcpdac.configuration import config
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger

global logger
global connex_app


def get_app_logger():
    global logger
    return logger


def init_logging():
    global logger
    logger = get_logger('tb-gcp-dac')
    logger.info("Logger initialised")


def init_connex_app():
    basedir = os.path.abspath(os.path.dirname(__file__))

    global connex_app
    connex_app = connexion.App(__name__, specification_dir=basedir)

    app = connex_app.app
    app.config.update(
        CELERY_BROKER_URL=config.environment_helper.get_celery_broker_url(),
        CELERY_RESULT_BACKEND=config.environment_helper.get_celery_result_backend(),
    )

    Marshmallow(app)


def init_gunicorn_logger():
    gunicorn_logger = get_logger("gunicorn.info")

    global connex_app
    connex_app.app.logger.handlers = gunicorn_logger.handlers
    connex_app.app.logger.setLevel(gunicorn_logger.level)


def init():
    config.init()
    init_logging()


# ===== init app =====
init()
init_connex_app()
init_gunicorn_logger()


# Run app
connex_app.add_api('openapi.yml', strict_validation=False)


if __name__ == "__main__":
    connex_app.run(port=config.environment_helper.get_app_port(), debug=config.environment_helper.get_debug_state())






