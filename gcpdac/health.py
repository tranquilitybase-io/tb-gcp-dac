"""
Health check: Very basic health check, can extend in future
"""

from gcpdac.extendedSchemas import HealthSchema

def check():
    # simple check that server is working. returns 200 on success

    status = { "status": "Healthy" }

    schema = HealthSchema()
    data = schema.dump(status)
    return data
