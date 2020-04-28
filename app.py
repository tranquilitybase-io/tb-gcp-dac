import logging
import os

# https://realpython.com/flask-connexion-rest-api/
# https://github.com/realpython/materials/tree/master/flask-connexion-rest-part-4
from celery import Celery

import config

print("DEBUG: {}".format(os.environ['DEBUG']))

# Get the application instance
connex_app = config.connex_app

# connect logging between gunicorn and Flask
# gunicorn_logger = logging.getLogger("gunicorn.error")
gunicorn_logger = logging.getLogger("gunicorn.info")
connex_app.app.logger.handlers = gunicorn_logger.handlers
connex_app.app.logger.setLevel(gunicorn_logger.level)

# Read the swagger.yml file to configure the endpoints
# connex_app.add_api('swagger.yml', strict_validation=True)
connex_app.add_api('openapi.yml', strict_validation=False)

# celery = make_celery(connex_app)
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(connex_app.app)

if __name__ == "__main__":
    connex_app.run(port=3100, debug=os.environ['DEBUG'])


