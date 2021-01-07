import os
import connexion
import itertools
from flask_marshmallow import Marshmallow

from src.main.python.tranquilitybase.lib.common.local_logging import get_logger

logger = get_logger('tb-gcp-dac')
logger.info("Logger initialised")

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
DEFAULT_SHELL="/bin/bash"

connex_app = connexion.App(__name__, specification_dir=basedir + "/.")
counter = itertools.count()

app = connex_app.app
ma = Marshmallow(app)


