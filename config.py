import os
import connexion
from flask_marshmallow import Marshmallow

from gcpdac.local_logging import get_logger
from gcpdac.utils import setDefaultGoogleCloudProject

logger = get_logger()
logger.info("Logger initialised")

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
DEFAULT_SHELL="/bin/bash"

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

ma = Marshmallow(app)

setDefaultGoogleCloudProject()


