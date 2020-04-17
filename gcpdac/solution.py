"""
This is the solution module and supports all the ReST actions for the
solution collection
"""

from pprint import pprint
from gcpdac import models

def create(solution):
    """
    reates a new solution based on the passed in solution data

    :param solution:  solution to create
    :return: 201 on success, solutionResponse: solution created
    """

    pprint(solution)

    # Serialize and return the newly created solution in the response
    schema = models.SolutionResponseSchema()
    folderId = "TESTFOLDERID"
    solutionResponse = {"id": solution.get("id"), "name": solution.get("name"), "folderId": folderId}

    data = schema.dump(solutionResponse)

    return data, 201
