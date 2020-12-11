
# add the following variables to test in a particular gcp environment
workspaceProjectId = ""  # a solution workspace project id
deploymentProjectId = "" #  a solution environment project id
activator_git_url = "" # git url for an external activator
base_folder_id = "" # tranquility base folder
teamCloudIdentityGroup = "" # valid cloud identity group
team_members = [
    {
        "role": {
            "name": "admin",
            "cloudIdentityGroup": "ADD HERE",
            "id": 1,
            "description": "eagle console admin role"
        },
        "user": {
            "lastName": "ADD_HERE",
            "email": "ADD_HERE",
            "id": 1,
            "firstName": "ADD_HERE",
            "isAdmin": False,
            "showWelcome": True
        },
        "id": 2
    }
]
