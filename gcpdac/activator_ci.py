import json

import config
from gcpdac.shell_utils import call_jenkins

logger = config.logger


def create_activator(activatordata):
    activator_id = activatordata.get("id")
    logger.debug("activator is %s", activator_id)
    solution_id = activatordata.get("solutionId")
    workspace_project_id = activatordata.get("workspaceProjectId") # get from tf state bucket?
    ec_config = config.read_config_map()
    eagle_project_id = ec_config['ec_project_name']



    # repo_name = "activator_{}_workspace".format(activator_id)
    # workspace_project_id = response["tf_outputs"]["workspace_project"]["value"]["project_id"]
    # create_repo(repo_name, workspace_project_id, eagle_project_id)

    # create terraform vars file
    # check vars file into repo
    # check repo for result file created by Jenkins CI

    # OR

    # create terraform vars file

    # ec_config = config.read_config_map()
    # TODO get jenkins url from ec_config ??

    # activator_name = activatordata.get("name")
    git_repo_url = activatordata.get("activatorGitUrl")
    # call Jenkins CI directly with vars file
    call_jenkins(git_repo_url)

    # TODO add check of jenkins result

    return {"return_code": 0}


def delete_activator(activatordata):
    # TODO place holder to call Jenkins

    return {"return_code": 0}
