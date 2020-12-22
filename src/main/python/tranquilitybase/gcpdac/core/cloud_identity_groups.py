from flask import Response

import requests

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))


def read_all():
    logger.debug("read_all")
    try:
        r: Response = requests.get("https://cloudidentity.googleapis.com/v1/groups")
        logger.debug("response is {} ".format(r))
        data = r.json()
        logger.debug("response data is {} ".format(data))
        groups = data["groups"]
        for group in groups:
            logger.debug("group is {} ".format(group))

        return data
    except Exception as e:
        logger.debug("error generating meta data {} ".format(e))
        return 500

