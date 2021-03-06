from typing import Any, Union, Tuple, Generator, Optional

from jenkinsapi.build import Build
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.job import Job

from src.main.python.tranquilitybase.gcpdac.celery_worker.tasks.jenkins.constants import JOB_UNIQUE_ID
from src.main.python.tranquilitybase.gcpdac.configuration.helpers.jenkinshelper import JenkinsHelper

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger, get_frame_name
logger = get_logger(get_frame_name(inspect.currentframe()))


def get_server_instance():
    server = Jenkins(JenkinsHelper.jenkins_base_url, username=JenkinsHelper.jenkins_user, password=JenkinsHelper.jenkins_password)
    return server


# Get job build from given job params
def get_job_build(job_name, job_params: dict) -> Optional[Build]:
    try:
        jenkins = get_server_instance()

        job_instance: Job = jenkins[job_name]
        logger.debug('Job Name:%s' % (job_instance.name))
        logger.debug('Job Description:%s' % (job_instance.get_description()))
        logger.debug('Is Job running:%s' % (job_instance.is_running()))
        logger.debug('Is Job enabled:%s' % (job_instance.is_enabled()))
        build_ids = job_instance.get_build_ids()

        for build_id in build_ids:
            logger.debug("build id {}".format(build_id))
            build = job_instance.get_build(build_id)
            build_params: dict = build.get_params()
            logger.debug("build params {}".format(build_params))
            logger.debug("job params {}".format(job_params))
            if build_params[JOB_UNIQUE_ID] == job_params[JOB_UNIQUE_ID]:
                logger.debug("Matched build on job unique id")
                return build
            else:
                logger.debug("Could not find a build matching job unique id")

        return None
    except Exception as ex:
        logger.debug("Exception: {0}".format(ex))

    return None


def format_jenkins_url(jenkins_params, jenkins_url):
    for key in jenkins_params:
        value = jenkins_params[key]
        jenkins_url = "{jenkins_url}&{key}={value}".format(jenkins_url=jenkins_url, key=key, value=value)
    return jenkins_url


def get_all_job_details():
    try:
        jenkins = get_server_instance()
        jobs: Generator[Union[Tuple[str, Job], Tuple[Any, Job]], Any, None] = jenkins.get_jobs()
        logger.debug("jobs type is {}".format(type(jobs)))

        for job_name, job_instance in jobs:
            logger.debug('Job Name:%s' % (job_instance.name))
            logger.debug('Job Description:%s' % (job_instance.get_description()))
            logger.debug('Is Job running:%s' % (job_instance.is_running()))
            logger.debug('Is Job enabled:%s' % (job_instance.is_enabled()))
            build_ids = jenkins[job_name].get_build_ids()
            for build_id in build_ids:
                logger.debug("build id {}".format(build_id))
                build = jenkins[job_name].get_build(build_id)
                get_build_details(build)
        return jobs
    except Exception as ex:
        logger.debug("Exception: {0}".format(ex))


def get_build_details(build):
    # https://jenkinsapi.readthedocs.io/en/latest/build.html
    artifacts = build.get_artifacts()
    for artifact in artifacts:
        logger.debug("artifact file name {}".format(artifact.filename))
        logger.debug("artifact data {}".format(artifact.get_data()))
    build_params = build.get_params()
    logger.debug("build params {}".format(build_params))
    for build_param in build_params:
        logger.debug("build param key {}".format(build_param))
        logger.debug("build param value{}".format(build_params[build_param]))
    logger.debug("build url {}".format(build.get_build_url()))

    logger.debug("build is running {}".format(build.is_running()))

    logger.debug("build is good {}".format(build.is_good()))
    if build.has_resultset():
        logger.debug("build resultset {}".format(build.get_resultset()))
        logger.debug("build results url {}".format(build.get_result_url()))
    else:
        logger.debug("No result set")
    causes = build.get_causes()
    for cause in causes:
        logger.debug("build param cause {}".format(cause))


def get_plugin_details():
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        logger.debug("Short Name:%s" % (plugin.shortName))
        logger.debug("Long Name:%s" % (plugin.longName))
        logger.debug("Version:%s" % (plugin.version))
        logger.debug("URL:%s" % (plugin.url))
        logger.debug("Active:%s" % (plugin.active))
        logger.debug("Enabled:%s" % (plugin.enabled))
