from datetime import datetime

from flask_marshmallow import Schema
from marshmallow import fields

class ModelTools():

    @staticmethod
    def get_utc_epoch():
        return datetime.utcnow().strftime('%s')

    @staticmethod
    def get_utc_timestamp():
        return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    @staticmethod
    def datetime_as_string(dt):
        if dt is None:
            return datetime.utcnow().strftime(("%Y-%m-%d %H:%M:%S"))
        else:
            return dt.strftime("%Y-%m-%d %H:%M:%S")

class SolutionResponseSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    folderId = fields.Str()

