from src.main.python.tranquilitybase.lib.common.utils import labellize
from tranquilitybase.gcpdac.functional.config import base_folder_id, team_members

solution_id = 1001
business_unit = 'BU-1'
cost_code = 'CC-1'
deployment_folder_id = base_folder_id
team_members = team_members
environments = [
    {'name':'Development',
     'id': 1,
     'sharedVPCProjectId': 'dummy'
     },
    {'name':'Production',
     'id': 4,
     'sharedVPCProjectId': 'dummy'
     }
]
environment_names = map(lambda x : x['name'], environments)
processed_environments = map(labellize, environment_names)
solution_name = 'solutionone'
solution_json = {
    'id': solution_id,
    'name': solution_name,
    'description': 'solution one description',
    'businessUnit': business_unit,
    'costCentre': cost_code,
    'ci': 'jenkins',
    'cd': 'jenkins',
    'sourceControl': 'git',
    'deploymentFolderId': deployment_folder_id,
    'environments': environments,
    'active': True,
    'favourite': True,
    "teamId": 1,
    "team": {
        "lastUpdated": "2020-03-01 12:34:56",
        "businessUnitId": 1,
        "teamMembers": team_members,
        "businessUnit": {
            "name": "Modern Apps",
            "isActive": True,
            "id": 1,
            "description": "Modern Apps"
        },
        "isActive": True,
        "id": 1,
        "description": "All Developers",
        "name": "Developers"
    },
    'lastUpdated': '2020-04-21T08:30:52+00:00'
}


def get_payload():
    return solution_json


def get_solutionId():
    return solution_id