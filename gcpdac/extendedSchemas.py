from marshmallow import Schema, fields, pre_load, post_load, pre_dump, post_dump, pprint

class HealthSchema(Schema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    status = fields.Str()

