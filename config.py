import os
from typing import Dict, List, Any, Union, Hashable

import connexion
import yaml
from flask_marshmallow import Marshmallow
from google.cloud import storage

def setDefaultGoogleCloudProject():
    with open('/app/ec-config.yaml') as f:
        try:
            data: dict = yaml.load(f, Loader=yaml.FullLoader)
            GOOGLE_CLOUD_PROJECT = data.get("ec_project_name")
            if not GOOGLE_CLOUD_PROJECT:
                raise ValueError("No GOOGLE_CLOUD_PROJECT set for Flask application")
            print(data)
        except yaml.YAMLError as exc:
            raise SystemError("Failed to parse EC YAML after successfully opening")
    print("GOOGLE_CLOUD_PROJECT: {}".format(GOOGLE_CLOUD_PROJECT))
    storage.Client(project=GOOGLE_CLOUD_PROJECT)

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
DEFAULT_SHELL="/bin/bash"

connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app

ma = Marshmallow(app)

setDefaultGoogleCloudProject()


