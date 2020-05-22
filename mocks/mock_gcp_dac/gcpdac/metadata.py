# Module to serve metadata endpoint
import config
from gcpdac.extendedSchemas import MetadataSchema


def read_all():
    # simple return some metadata, key and value pairs. returns 200 on success

    data = {
        "root_folder_id": "rootfolderid"
    }

    print(data)
    schema = MetadataSchema()
    data = schema.dump(data)
    return data, 200