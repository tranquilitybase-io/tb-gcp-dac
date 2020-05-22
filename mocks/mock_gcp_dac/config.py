import os
import yaml
import connexion
import itertools
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))
print("basedir: {}".format(basedir))
DEFAULT_SHELL="/bin/bash"

connex_app = connexion.App(__name__, specification_dir=basedir + "/.")
counter = itertools.count()

app = connex_app.app
ma = Marshmallow(app)


ec_config = None


def read_config_map():
    # Returns the EC configuration as a dictionary

    try:
        with open("gcpdac/ec-config.yaml", 'r') as stream:
            try:
                ec_config = yaml.safe_load(stream)
                return ec_config
            except yaml.YAMLError as exc:
                logger.exception("Failed to parse EC YAML after successfully opening - {}".format(exc))
                raise
    except Exception:
        print("Failed to load EC YAML file")
        raise

    return ec_config
