import os

import config
from gcpdac.constants import JENKINS_BASE_URL, JENKINS_TOKEN, JENKINS_DEPLOY_ACTIVATOR_JOB, DEPLOYMENT_PROJECT_ID, \
    ACTIVATOR_GIT_REPO_URL
from gcpdac.exceptions import DacValidationError, DacJenkinsError
from gcpdac.shell_utils import create_repo, copy_repo, call_jenkins
from gcpdac.utils import sanitize

logger = config.logger


def create_application(applicationdata):
    application_id = applicationdata.get("id")
    application_name = applicationdata.get("name")
    logger.debug("application is %s", application_id)
    logger.debug("application data is {}".format(applicationdata))
    application_git_url, workspace_project_id, deployment_environment, deployment_project_id = validateInput(
        applicationdata)
    try:
        jenkins_base_url = os.environ[JENKINS_BASE_URL]
    except Exception as e:
        print(e)
        raise DacJenkinsError(
            "Jenkins environment variables not set. Check {} are set".format(JENKINS_BASE_URL))
    ec_config = config.ec_config
    eagle_project_id = ec_config['ec_project_name']

    repo_name = "activator-{}".format(application_name)
    repo_name = sanitize(repo_name)

    create_repo_response = create_repo(repo_name, workspace_project_id, eagle_project_id)
    logger.debug("Create repo response code {}".format(create_repo_response))

    copy_repo_response = copy_repo(application_git_url, repo_name, workspace_project_id, eagle_project_id)
    logger.debug("Copy repo response code {}".format(copy_repo_response))
    jenkins_token = JENKINS_TOKEN
    jenkins_deploy_activator_job = JENKINS_DEPLOY_ACTIVATOR_JOB
    # jenkins_job_instance_name = random_element(12)  # TODO exact format of name to be agreed on

    jenkins_url = "{jenkins_base_url}/buildByToken/buildWithParameters?job={jenkins_deploy_activator_job}&token={jenkins_token}".format(
        jenkins_base_url=jenkins_base_url,
        jenkins_deploy_activator_job=jenkins_deploy_activator_job,
        jenkins_token=jenkins_token)
    jenkins_params = {}
    # TODO re-add this when Jenkins job supports GSR
    # git_repo_url = "https://source.developers.google.com/p/{workspace_project_id}/r/{repo_name}".format(
    #     workspace_project_id=workspace_project_id, repo_name=repo_name)
    jenkins_params[ACTIVATOR_GIT_REPO_URL] = application_git_url
    jenkins_params[DEPLOYMENT_PROJECT_ID] = deployment_project_id
    # jenkins_params["jenkins_job_instance_name"] = jenkins_job_instance_name
    call_jenkins_response = call_jenkins(jenkins_url, jenkins_params)
    logger.debug("Call Jenkins response code {}".format(call_jenkins_response))

    # TODO check results of jenkins job

    response = {}
    response["repo_name"] = repo_name

    return response


def validateInput(applicationdata):
    workspace_project_id = applicationdata.get("workspaceProjectId", None)
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
    # TODO not implemented yet - will be another call to jenkins

    return {"return_code": 0}
