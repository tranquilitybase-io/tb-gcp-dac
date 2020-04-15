"""
Health check: Very basic health check, can extend in future
"""

# 3rd party modules
from gcpdac.extendedSchemas import HealthSchema

def check():
    """
    :return:       200
    """

    status = { "status": "Healthy" }

    schema = HealthSchema()
    data = schema.dump(status)
    return data
