import time
import traceback

import requests
from requests import Response

import config
from gcpdac.constants import JENKINS_TOKEN, JENKINS_DEPLOY_ACTIVATOR_JOB, DEPLOYMENT_PROJECT_ID, \
    ACTIVATOR_GIT_REPO_URL, ACTIVATOR_PARAMS, JOB_UNIQUE_ID
from gcpdac.exceptions import DacValidationError, DacError
from gcpdac.jenkins_utils import get_job_build, format_jenkins_url
from gcpdac.shell_utils import create_repo, copy_repo
from gcpdac.utils import sanitize, random_element

logger = config.logger


def create_application(applicationdata):
    application_id = applicationdata.get("id")
    application_name = applicationdata.get("name")
    logger.debug("application is %s", application_id)
    logger.debug("application data is {}".format(applicationdata))
    application_git_url, workspace_project_id, deployment_environment, deployment_project_id, mandatory_variables, optional_variables = validateInput(
        applicationdata)
    logger.debug("deployment_environment {}".format(deployment_environment))
    jenkins_base_url = config.JENKINS_BASE_URL
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

    # "jenkins-master-svc.cicd/buildByToken/buildWithParameters?job=Activator-Pipeline&token=activatorbuild&repourl=https://github.com/tranquilitybase-io/tb-gcp-hpc-activator.git&projectid=development-zzmnjt-f9e64e73"
    jenkins_url = "{jenkins_base_url}/buildByToken/buildWithParameters?job={jenkins_deploy_activator_job}&token={jenkins_token}".format(
        jenkins_base_url=jenkins_base_url,
        jenkins_deploy_activator_job=jenkins_deploy_activator_job,
        jenkins_token=jenkins_token)
    logger.info("jenkins_url before params added {}".format(jenkins_url))
    jenkins_params = {}
    # TODO re-add this when Jenkins job supports GSR
    # git_repo_url = "https://source.developers.google.com/p/{workspace_project_id}/r/{repo_name}".format(
    #     workspace_project_id=workspace_project_id, repo_name=repo_name)
    # TODO pull from input
    activator_params = get_activator_params(mandatory_variables, optional_variables)

    job_unique_id = random_element(num_chars=12)

    jenkins_params[ACTIVATOR_GIT_REPO_URL] = application_git_url
    logger.info("application_git_url {}".format(application_git_url))
    jenkins_params[DEPLOYMENT_PROJECT_ID] = deployment_project_id
    logger.info("deployment_project_id {}".format(deployment_project_id))
    jenkins_params[ACTIVATOR_PARAMS] = activator_params
    logger.info("activator_params {}".format(activator_params))
    jenkins_params[JOB_UNIQUE_ID] = job_unique_id
    logger.info("job_unique_id {}".format(job_unique_id))

    jenkins_url = format_jenkins_url(jenkins_params, jenkins_url)
    logger.info("jenkins_url {}".format(jenkins_url))

    response = {}
    payload = {}
    payload["jenkins_job_params"] = jenkins_params
    # TODO add more details to response

    try:
        r: Response = requests.post(jenkins_url)
        logger.debug("response is {} ".format(r))

        # sleep to wait for build to be created
        time.sleep(10)
        job_build = get_job_build(jenkins_deploy_activator_job, jenkins_params)
        if job_build != None:
            while job_build.is_running():
                # TODO add check to give up on Jenkins job if takes too long
                logger.debug("Job Build {} is still running".format(job_build.buildno))
                time.sleep(60)
            logger.debug("Job build finished")
            logger.debug("Build Status {}".format(job_build.get_status()))
            build_url = job_build.get_build_url()
            logger.debug("Build URL {}".format(build_url))
            logger.debug("Result URL {}".format(job_build.get_result_url()))
            # http://10.0.1.9/job/Activator-Pipeline/17/api/json
            build_url_json = build_url + "/api/json"
            logger.debug("Build URL JSON {}".format(build_url_json))
            r: Response = requests.get(build_url_json)
            results: dict = r.json()
            logger.debug("results {}".format(results))
            build_result = results["result"]
            logger.debug("result {}".format(build_result))
            if build_result == "SUCCESS":
                response["return_code"] = 0
            else:
                response["return_code"] = 999
        else:
            logger.debug("No job build created")
            response["return_code"] = 999

    except Exception as ex:
        logger.debug(traceback.format_exc())
        traceback.format_exc()
        raise DacError(ex, "Error occurred in deploy activator")

    response["payload"] = payload
    return response


def get_activator_params(mandatory_variables, optional_variables):
    # TODO convert input dicts to key-value pair string

    return "a=123,b=456"


def validateInput(applicationdata):
    workspace_project_id = applicationdata.get("workspaceProjectId", None)
    deployment_project_id = applicationdata.get("deploymentProjectId", None)
    activator_git_url = applicationdata.get("activatorGitUrl", None)
    deployment_environment_object = applicationdata.get("deploymentEnvironment", None)
    mandatory_variables = applicationdata.get("mandatoryVariables", None)
    optional_variables = applicationdata.get("optionalVariables", None)
    deployment_environment = None
    if deployment_environment_object != None:
        deployment_environment = deployment_environment_object.get("name", None)

    if (workspace_project_id == None or activator_git_url == None or
            deployment_environment == None or deployment_project_id == None):
        error_msg = "Workspace Project ID, activator Git URL, deployment environment and deployment project id must be supplied"
        logger.info(error_msg)
        raise DacValidationError(applicationdata, error_msg)
    return activator_git_url, workspace_project_id, deployment_environment, deployment_project_id, mandatory_variables, optional_variables


def delete_application(applicationdata):
    # TODO not implemented yet - will be another call to jenkins

    return {"return_code": 0}
