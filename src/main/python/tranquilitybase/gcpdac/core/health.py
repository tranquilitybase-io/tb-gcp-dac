from src.main.python.tranquilitybase.gcpdac.core.extendedSchemas import HealthSchema


def check():
    status = {"status": "Healthy"}
    schema = HealthSchema()
    data = schema.dump(status)
    return data
