# Module to serve metadata endpoint
from gcpdac.extendedSchemas import MetadataSchema


def read_all():
    # simple return some metadata, key and value pairs. returns 200 on success

    data = {
        "root_folder_id": "rootfolderid",
        "shared_vpc_host_project": "shared_vpc_host_project"
    }

    schema = MetadataSchema(many=False)
    data = schema.dump(data)
    return data, 200
