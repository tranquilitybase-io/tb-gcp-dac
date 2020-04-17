import json
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

    @staticmethod
    def load_json_array(s):
        try:
            return json.loads(s)
        except Exception as e:
            return []

    @staticmethod
    def json_dump(obj):
        #return json.dumps(obj, indent=2, sort_keys=True)
        return json.dumps(obj)

    # simple redact function, used prior to logging
    @staticmethod
    def redact_dict(my_dict):
        new_dict = my_dict.copy()
        new_dict['username'] = "XXXXX"
        new_dict['password'] = "XXXXX"
        return new_dict

class SolutionResponseSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    folderId = fields.Str()

