# Module to serve metadata endpoint
import config
from gcpdac.extendedSchemas import MetadataSchema
logger = config.logger

def get_metadata_from_config():
    logger.debug("get_metadata_from_config")
    ec_config = config.read_config_map()
    data = { }
    data['root_folder_id'] = ec_config.get('activator_folder_id').replace("folders/","")
    return data


def read_all():
    # simple return some metadata, key and value pairs. returns 200 on success
    logger.debug("read_all")
    data = get_metadata_from_config()
    logger.debug(data)
    schema = MetadataSchema()
    data = schema.dump(data)
    return data, 200
