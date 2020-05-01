import logging
import os

import config
from celery_worker import add_two_numbers

print("DEBUG: {}".format(os.environ['DEBUG']))

logger = config.logger

connex_app = config.connex_app

# gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn.info")
connex_app.app.logger.handlers = gunicorn_logger.handlers
connex_app.app.logger.setLevel(gunicorn_logger.level)

connex_app.add_api('openapi.yml', strict_validation=False)

celery = config.get_celery()

# TODO check Celery worker is working
result = add_two_numbers.delay(23, 42)
result.wait()

if __name__ == "__main__":
    connex_app.run(port=3100, debug=os.environ['DEBUG'])
