import config
from gcpdac.exceptions import DacValidationError
from gcpdac.shell_utils import create_repo, copy_repo
from gcpdac.utils import sanitize

logger = config.logger


def create_activator(activatordata):
    activator_id = activatordata.get("id")
    activator_name = activatordata.get("name")
    # activator_description = activatordata.get("description")
    logger.debug("activator is %s", activator_id)
    # solution_id = activatordata.get("solutionId")
    activator_git_url, workspace_project_id = validateInput(activatordata)

    ec_config = config.read_config_map()
    eagle_project_id = ec_config['ec_project_name']

    repo_name = "activator-{}".format(activator_name)
    repo_name = sanitize(repo_name)

    create_repo(repo_name, workspace_project_id, eagle_project_id)

    copy_repo(activator_git_url, repo_name, workspace_project_id, eagle_project_id)

    # TODO call jenkins job

    # TODO check results of jenkins job
    response = {}
    response["repo_name"] = repo_name

    # return {"return_code": 0, "repo_name": repo_name}
    return response


def validateInput(activatordata):
    workspace_project_id = activatordata.get("workspaceProjectId", None)  # TODO get from tf state bucket?
    activator_git_url = activatordata.get("activatorGitUrl", None)
    if (workspace_project_id == None or activator_git_url == None):
        error_msg = "Workspace Project ID and Activator Git URL must be supplied"
        logger.info(error_msg)
        raise DacValidationError(activatordata, error_msg)
    return activator_git_url, workspace_project_id


def delete_activator(activatordata):
    # TODO not implemented yet

    return {"return_code": 0}
