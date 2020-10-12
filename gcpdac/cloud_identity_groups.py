import config

logger = config.logger


def read_all():
    logger.debug("read_all")
    # TODO retrieve from GCP
    data = {}
    return data, 200
