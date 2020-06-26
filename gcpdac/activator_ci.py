import config
from gcpdac.shell_utils import create_repo, copy_repo
from gcpdac.utils import sanitize

logger = config.logger


def create_activator(activatordata):
    activator_id = activatordata.get("id")
    activator_name = activatordata.get("name")
    # activator_description = activatordata.get("description")
    logger.debug("activator is %s", activator_id)
    # solution_id = activatordata.get("solutionId")
    workspace_project_id = activatordata.get("workspaceProjectId")  # get from tf state bucket?
    activator_get_url = activatordata.get("activatorGitUrl")

    ec_config = config.read_config_map()
    eagle_project_id = ec_config['ec_project_name']

    repo_name = "activator-{}".format(activator_name)
    repo_name = sanitize(repo_name)

    create_repo(repo_name, workspace_project_id, eagle_project_id)

    copy_repo(activator_get_url, repo_name, workspace_project_id, eagle_project_id)

    # TODO call jenkins job

    # TODO check results of jenkins job

    return {"return_code": 0, "repo_name": repo_name}


def delete_activator(activatordata):
    # TODO not implemented yet

    return {"return_code": 0}
