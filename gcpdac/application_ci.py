import json

import config
from gcpdac.shell_utils import call_jenkins

logger = config.logger


def create_application(applicationdata):
    application_id = applicationdata.get("id")
    logger.debug("application is %s", application_id)
    solution_id = applicationdata.get("solutionId")
    workspace_project_id = applicationdata.get("workspaceProjectId") # get from tf state bucket?
    ec_config = config.ec_config
    eagle_project_id = ec_config['ec_project_name']



    # repo_name = "application_{}_workspace".format(application_id)
    # workspace_project_id = response["tf_outputs"]["workspace_project"]["value"]["project_id"]
    # create_repo(repo_name, workspace_project_id, eagle_project_id)

    # create terraform vars file
    # check vars file into repo
    # check repo for result file created by Jenkins CI

    # OR

    # create terraform vars file

    # ec_config = config.ec_config
    # TODO get jenkins url from ec_config ??

    # application_name = applicationdata.get("name")
    git_repo_url = applicationdata.get("activatorGitUrl")
    # call Jenkins CI directly with vars file
    call_jenkins(git_repo_url)

    # TODO add check of jenkins result

    return {"return_code": 0}


def delete_application(applicationdata):
    # TODO place holder to call Jenkins

    return {"return_code": 0}
