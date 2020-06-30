import config
from gcpdac.exceptions import DacValidationError
from gcpdac.shell_utils import create_repo, copy_repo, call_jenkins
from gcpdac.utils import sanitize

logger = config.logger


def create_application(applicationdata):
    application_id = applicationdata.get("id")
    application_name = applicationdata.get("name")
    # application_description = applicationdata.get("description")
    logger.debug("application is %s", application_id)
    # solution_id = applicationdata.get("solutionId")
    application_git_url, workspace_project_id, deployment_environment, deployment_project_id = validateInput(applicationdata)

    ec_config = config.read_config_map()
    eagle_project_id = ec_config['ec_project_name']

    repo_name = "activator-{}".format(application_name)
    repo_name = sanitize(repo_name)

    create_repo(repo_name, workspace_project_id, eagle_project_id)

    copy_repo(application_git_url, repo_name, workspace_project_id, eagle_project_id)

    # TODO call jenkins job
    call_jenkins(repo_name, deployment_environment, deployment_project_id)

    # TODO check results of jenkins job
    response = {}
    response["repo_name"] = repo_name

    # return {"return_code": 0, "repo_name": repo_name}
    return response


def validateInput(applicationdata):
    workspace_project_id = applicationdata.get("workspaceProjectId", None)  # TODO get from tf state bucket?
    activator_git_url = applicationdata.get("activatorGitUrl", None)
    deployment_environment = applicationdata.get("deploymentEnvironment", None)
    deployment_project_id = applicationdata.get("deploymentProjectId", None)

    if (workspace_project_id == None or activator_git_url == None or
            deployment_environment == None or deployment_project_id == None):
        error_msg = "Workspace Project ID, activator Git URL, deployment environment and deployment project id must be supplied"
        logger.info(error_msg)
        raise DacValidationError(applicationdata, error_msg)
    return activator_git_url, workspace_project_id, deployment_environment, deployment_project_id


def delete_application(applicationdata):
    # TODO not implemented yet

    return {"return_code": 0}
