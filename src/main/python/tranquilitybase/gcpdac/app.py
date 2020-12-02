import logging
import os

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
import connexion
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app




# from src.main.python.tranquilitybase.gcpdac import config
#
# print("DEBUG: {}".format(os.environ['DEBUG']))
#
# logger = config.logger
#
# connex_app = config.connex_app
#
# gunicorn_logger = logging.getLogger("gunicorn.info")
# connex_app.app.logger.handlers = gunicorn_logger.handlers
# connex_app.app.logger.setLevel(gunicorn_logger.level)
#
# connex_app.add_api('openapi.yml', strict_validation=True)
#
# celery = config.get_celery()
#
# if __name__ == "__main__":
#     connex_app.run(port=os.environ['APP_PORT'], debug=os.environ['DEBUG'])
