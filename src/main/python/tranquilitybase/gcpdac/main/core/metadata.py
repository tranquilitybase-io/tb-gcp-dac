# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger, get_frame_name
logger = get_logger(get_frame_name(inspect.currentframe()))

from src.main.python.tranquilitybase.gcpdac.main.core.schemas.extendedSchemas import MetadataSchema
from src.main.python.tranquilitybase.gcpdac.configuration.helpers.eaglehelper import EagleConfigHelper


def get_metadata_from_config():
    logger.debug("get_metadata_from_config")
    ec_config = EagleConfigHelper.config_dict
    data = {}
    data['root_folder_id'] = str(ec_config.get('activator_folder_id')).replace("folders/", "")
    data['shared_vpc_host_project'] = str(ec_config.get('shared_vpc_host_project'))
    return data


def read_all():
    # simple return some metadata, key and value pairs. returns 200 on success
    logger.debug("read_all")
    data = get_metadata_from_config()
    logger.debug(data)
    schema = MetadataSchema()
    data = schema.dump(data)
    return data, 200
