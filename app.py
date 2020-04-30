import logging
import os

from celery_worker import add_together_two

import config

print("DEBUG: {}".format(os.environ['DEBUG']))

logger = config.logger

# Get the application instance
connex_app = config.connex_app

# connect logging between gunicorn and Flask
# gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn.info")
connex_app.app.logger.handlers = gunicorn_logger.handlers
connex_app.app.logger.setLevel(gunicorn_logger.level)

# Read the openapi.yml file to configure the endpoints
connex_app.add_api('openapi.yml', strict_validation=False)

celery = config.get_celery()

result = add_together_two.delay(23, 42)
result.wait()

if __name__ == "__main__":
    connex_app.run(port=3100, debug=os.environ['DEBUG'])
