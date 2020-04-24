from flask_marshmallow import Schema
from marshmallow import fields

class SolutionResponseSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    folderId = fields.Str()

