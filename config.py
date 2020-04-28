import os
import connexion
from flask_marshmallow import Marshmallow
from gcpdac.utils import setDefaultGoogleCloudProject

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
DEFAULT_SHELL="/bin/bash"

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

ma = Marshmallow(app)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

setDefaultGoogleCloudProject()


