"""
Health check: Very basic health check, can extend in future
"""

from gcpdac.extendedSchemas import HealthSchema

def check():
    """
    :return: 200 on success
    """

    status = { "status": "Healthy" }

    schema = HealthSchema()
    data = schema.dump(status)
    return data
