from src.main.python.tranquilitybase.gcpdac.main.core.schemas.extendedSchemas import HealthSchema


def check():
    status = {"status": "Healthy"}
    schema = HealthSchema()
    data = schema.dump(status)
    return data
