import json
import time
import traceback

import requests

from typing import Optional
from requests import Response
from jenkinsapi.build import Build
from jenkinsapi.artifact import Artifact

from src.main.python.tranquilitybase.gcpdac.configuration.helpers.eaglehelper import EagleConfigHelper
from src.main.python.tranquilitybase.gcpdac.configuration.helpers.jenkinshelper import JenkinsHelper
from src.main.python.tranquilitybase.gcpdac.celery_worker.tasks.jenkins.constants import *
from src.main.python.tranquilitybase.gcpdac.main.core.exceptions.exceptions import DacValidationError, DacError
from src.main.python.tranquilitybase.gcpdac.celery_worker.tasks.jenkins.jenkins_utils import get_job_build, format_jenkins_url
from src.main.python.tranquilitybase.lib.common.utils import random_element

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger, get_frame_name
logger = get_logger(get_frame_name(inspect.currentframe()))


def create_application(applicationdata):
    application_id = applicationdata.get("id")
    application_name = applicationdata.get("name")
    logger.debug("application id is %s", application_id)
    logger.debug("application name is %s", application_name)
    logger.debug("application data is {}".format(applicationdata))

    workspace_project_id = applicationdata.get("workspaceProjectId", None)
    deployment_project_id = applicationdata.get("deploymentProjectId", None)
    application_git_url = applicationdata.get("activatorGitUrl", None)
    deployment_environment_object = applicationdata.get("deploymentEnvironment", None)
    mandatory_variables = applicationdata.get("mandatoryVariables", None)
    optional_variables = applicationdata.get("optionalVariables", None)

    deployment_environment = None
    shared_vpc_project_id = None
    if deployment_environment_object != None:
        deployment_environment = deployment_environment_object.get("name", None)
        shared_vpc_project_id = deployment_environment_object.get("sharedVPCProjectId", None)

    if (workspace_project_id == None or application_git_url == None or
            deployment_environment == None or deployment_project_id == None or shared_vpc_project_id == None):
        error_msg = "Workspace Project ID, activator Git URL, deployment environment, shared vpc project id and deployment project id must be supplied"
        logger.info(error_msg)
        raise DacValidationError(applicationdata, error_msg)

    logger.debug("deployment_environment {}".format(deployment_environment))

    jenkins_url = "{jenkins_base_url}/generic-webhook-trigger/invoke?job={jenkins_deploy_activator_job}&token={jenkins_token}".format(
        jenkins_base_url=(JenkinsHelper.jenkins_base_url),
        jenkins_deploy_activator_job=(JENKINS_DEPLOY_ACTIVATOR_JOB_WITH_JSON),
        jenkins_token=(JENKINS_TOKEN))
    logger.info("jenkins_url before params added {}".format(jenkins_url))

    job_unique_id = random_element(num_chars=20)
    jenkins_params: dict = {}
    jenkins_params[ACTIVATOR_GIT_REPO_URL] = application_git_url
    jenkins_params[DEPLOYMENT_PROJECT_ID] = deployment_project_id
    jenkins_params[JOB_UNIQUE_ID] = job_unique_id
    # TODO will be passed from Houston in some cases where a branch or tag needs to be used - for now default to main/master
    jenkins_params[ACTIVATOR_GIT_REPO_BRANCH] = "master"

    logger.info("deployment_project_id {}".format(deployment_project_id))
    logger.info("application_git_url {}".format(application_git_url))
    logger.info("job_unique_id {}".format(job_unique_id))

    environment_params = dict()
    environment_params["shared_vpc_project_id"] = shared_vpc_project_id
    environment_params["region"] = EagleConfigHelper.config_dict["region"]

    deployment_params = dict()
    deployment_params[ACTIVATOR_PARAMS] = get_activator_params(mandatory_variables, optional_variables)
    deployment_params[ENVIRONMENT_PARAMS] = environment_params

    jenkins_url = format_jenkins_url(jenkins_params, jenkins_url)
    logger.info("jenkins_url {}".format(jenkins_url))

    response = {}
    payload = {}

    try:
        activator_params_json = json.dumps(deployment_params)
        logger.debug("activator_params_json is {} ".format(activator_params_json))

        r: Response = requests.post(jenkins_url, data=activator_params_json)
        logger.debug("response is {} ".format(r))

        # sleep to wait for build to be created
        time.sleep(10)
        job_build: Optional[Build] = get_job_build(JENKINS_DEPLOY_ACTIVATOR_JOB_WITH_JSON, jenkins_params)
        if job_build is not None:
            while job_build.is_running():
                # TODO add check to give up on Jenkins job if takes too long
                logger.debug("Job Build {} is still running".format(job_build.buildno))
                time.sleep(60)
            logger.debug("Job build finished")
            logger.debug("Build Status {}".format(job_build.get_status()))
            build_url = job_build.get_build_url()
            logger.debug("Build URL {}".format(build_url))
            logger.debug("Result URL {}".format(job_build.get_result_url()))

            payload["activator_outputs"] = get_activator_outputs(job_build)

            build_url_json = build_url + "/api/json"
            logger.debug("Build URL JSON {}".format(build_url_json))
            r: Response = requests.get(build_url_json)
            results: dict = r.json()
            logger.debug("results {}".format(results))

            # will be either SUCCESS or FAILURE
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


    logger.debug("Payload is: {}".format(payload))
    response["payload"] = payload

    return response


def get_activator_outputs(job_build):
    activator_outputs = dict()
    try:
        logger.debug("Getting build artifacts")
        build_artifacts = job_build.get_artifacts()
        for build_artifact in build_artifacts:
            build_artifact: Artifact = build_artifact
            logger.debug("build_artifact.relative_path {}".format(build_artifact.relative_path))
            logger.debug("build_artifact.url {}".format(build_artifact.url))
            logger.debug("build_artifact.filename {}".format(build_artifact.filename))
            logger.debug("build_artifact.build {}".format(build_artifact.build))
            # look for activator_outputs.json artifact
            if build_artifact.filename == "activator_outputs.json":
                response: Response = requests.get(build_artifact.url)
                activator_outputs_text = response.text
                logger.debug("activator_outputs_text {}".format(activator_outputs_text))
                activator_outputs: dict = json.loads(activator_outputs_text)
                logger.debug("activator_outputs {}".format(activator_outputs))

    except Exception as ex:
        logger.debug("Exception getting artifacts: {0}".format(ex))

    return activator_outputs


def get_activator_params(mandatory_variables: list, optional_variables: list):
    activator_params: dict = {}
    for variable in mandatory_variables:
        activator_params[variable["key"]] = variable["value"]
    for variable in optional_variables:
        activator_params[variable["key"]] = variable["value"]

    return activator_params


def delete_application(applicationdata):
    # TODO not implemented yet - will be another call to jenkins

    return {"return_code": 0}
