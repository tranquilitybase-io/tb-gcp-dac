import logging
import os

# https://realpython.com/flask-connexion-rest-api/
# https://github.com/realpython/materials/tree/master/flask-connexion-rest-part-4
from celery import Celery
from tasks import add_together

import config

print("DEBUG: {}".format(os.environ['DEBUG']))

# Get the application instance
connex_app = config.connex_app

# connect logging between gunicorn and Flask
# gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn.info")
connex_app.app.logger.handlers = gunicorn_logger.handlers
connex_app.app.logger.setLevel(gunicorn_logger.level)

# Read the openapi.yml file to configure the endpoints
connex_app.add_api('openapi.yml', strict_validation=False)

# celery = make_celery(connex_app.app)

result = add_together.delay(23, 42)
result.wait()

if __name__ == "__main__":
    connex_app.run(port=3100, debug=os.environ['DEBUG'])


