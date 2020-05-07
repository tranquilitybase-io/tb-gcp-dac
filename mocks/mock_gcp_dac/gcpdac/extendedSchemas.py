from marshmallow import Schema, fields

class HealthSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    status = fields.Str()

class ResponseSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    id = fields.Int()
    deployed = fields.Bool()
    deploymentState = fields.Str()
    statusId = fields.Int()
    statusCode = fields.Str()
    statusMessage = fields.Str()
    taskId = fields.Int()
