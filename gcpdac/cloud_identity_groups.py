from flask import Response

import config
import requests

logger = config.logger


def read_all():
    logger.debug("read_all")
    r: Response = requests.get("https://cloudidentity.googleapis.com/v1/groups")
    logger.debug("response is {} ".format(r))
    data = r.json()
    logger.debug("response data is {} ".format(data))
    groups = data["groups"]
    for group in groups:
        logger.debug("group is {} ".format(group))

    return data



# TODO retrieve from GCP
    data = {}
    return data, 200
