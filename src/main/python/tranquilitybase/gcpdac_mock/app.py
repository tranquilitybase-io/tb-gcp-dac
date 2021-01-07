import os
import logging
from src.main.python.tranquilitybase.gcpdac_mock import config

print("DEBUG: {}".format(os.environ['DEBUG']))

connex_app = config.connex_app

# gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn.info")
connex_app.app.logger.handlers = gunicorn_logger.handlers
connex_app.app.logger.setLevel(gunicorn_logger.level)
connex_app.add_api('openapi.yml', strict_validation=False)

if __name__ == "__main__":
    connex_app.run(port=3100, debug=os.environ['DEBUG'])
