from marshmallow import Schema, fields

class HealthSchema(Schema):
    """
    Schema for health check.
    """
    def __init__(self, **kwargs):
        """
        Constructor for this class.
        """
        super().__init__(**kwargs)

    status = fields.Str()

class ResponseSchema(Schema):
    """
    Schema for HS Response.
    """
    def __init__(self, **kwargs):
        """
        Constructor for this class.
        """
        super().__init__(**kwargs)

    id = fields.Int()
    deployed = fields.Bool()
    deploymentState = fields.Str()
    statusId = fields.Int()
    statusCode = fields.Str()
    statusMessage = fields.Str()
    taskId = fields.Int()
