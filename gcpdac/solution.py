"""
This is the solution module and supports all the ReST actions for the
solution collection
"""

from pprint import pprint
from gcpdac import models

def create(solution):
    """
    This function creates a new solution based on the passed in solution data

    :param solution:  solution to create
    :return:             201 on success, TODO
    """

    pprint(solution)

    # Serialize and return the newly created application
    # in the response
    schema = models.SolutionResponseSchema()
    solutionResponse = dict(name="TEST")

    data = schema.dump(solutionResponse)

    return data, 201
