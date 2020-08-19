# add the following variables to test in a particular gcp environment
workspaceProjectId = "workspace-chaq7c-ksjs726s"  # a solution workspace project id
deploymentProjectId = "development-chaq7c-ksjs726s" #  a solution environment project id
activator_git_url = "https://source.developers.google.com/p/workspace-chaq7c-ksjs726s/r/activator-testapp" # git url for an external activator
base_folder_id = "302197932093" # tranquility base folder
team_members = [
    {
        "role": {
            "name": "admin",
            "cloudIdentityGroup": "ADD HERE",
            "id": 1,
            "description": "eagle console admin role"
        },
        "user": {
            "lastName": "Underhill",
            "email": "simon.underhill@gft.com",
            "id": 1,
            "firstName": "Simon",
            "isAdmin": False,
            "showWelcome": True
        },
        "id": 2
    }
]# deploymentProjectId = None
# workspaceProjectId = None
