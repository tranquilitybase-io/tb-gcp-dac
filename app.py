import os
import config
import logging
# https://realpython.com/flask-connexion-rest-api/
# https://github.com/realpython/materials/tree/master/flask-connexion-rest-part-4

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
connex_app.add_api('swagger.yml', strict_validation=False)

if __name__ == "__main__":
    connex_app.run(port=3100, debug=os.environ['DEBUG'])
