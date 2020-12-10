from marshmallow import Schema, fields


class HealthSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    status = fields.Str()


class MetadataSchema(Schema):
    """
    Schema for Metadata Response.
    """
    def __init__(self, **kwargs):
        """
        Constructor for this class.
        """
        super().__init__(**kwargs)

    root_folder_id = fields.Str()
    shared_vpc_host_project = fields.Str()

