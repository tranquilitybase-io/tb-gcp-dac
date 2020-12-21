from src.main.python.tranquilitybase.gcpdac.core.schemas.extendedSchemas import HealthSchema


def check():
    status = {"status": "Healthy"}
    schema = HealthSchema()
    data = schema.dump(status)
    return data
