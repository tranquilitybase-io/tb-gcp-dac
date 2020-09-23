import sys
import time
from typing import Any, Union, Tuple, Generator, Optional

import requests
from jenkinsapi.artifact import Artifact
from jenkinsapi.build import Build
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.job import Job

import config
from config import JENKINS_BASE_URL, JENKINS_ADMIN_USER, JENKINS_ADMIN_PASSWORD
from gcpdac import constants

logger = config.logger


##Define a function to give us all of our Jobs on our server
def getJenkinsJobs(server):
    # return server.get_jobs()
    # return server.jobs
    return server.keys()


##This next function has a LOT going on, so I'll comment as we go.
def runJenkinsJob(job, paramsMap):  ##Define a function to handle running our job
    if (len(job.get_params_list()) != len(sys.argv) - 3):  ##If we don't pass in enough arguments...
        print(
            "Error: Argument length mismatch. Please ensure that you're supplying enough arguments for the jenkins job.")
        exit()  ## ... exit the script.

    if (job.has_params()):  ## else, if that job has parameters
        builder = {}  ##we do some fancy magic to build our job.
        counter = 3  ##the first thing we want is arguement #3 from our command line
        for param in job.get_params_list():  # for each parameter the job has, set the command line arguement equal to it.
            builder[param] = sys.argv[counter]
            counter = counter + 1
        print("Starting job '" + job.name + "'.")  ##Let us know we're starting our job.
        job.invoke(None, False, False, 3, 15, builder, None, None)  ##Invoke the job from our wrapper library.

    else:
        job.invoke()  ##invoke the job with no parameters.


def blowup():  ##gives us some error output to help users the second time around.
    print("You need to specify a job name, task, and any arguements needed.")
    print("If you're trying to deploy jenkinsTestApp (version 2.0.0) to beta.")
    print("Try this: > Sinclair jenkinsTestApp deploy beta 2.0.0")
    exit()


def noJobs():
    print('Could not find the job that was entered.')


def get_server_instance():
    server = Jenkins(JENKINS_BASE_URL, username=JENKINS_ADMIN_USER, password=JENKINS_ADMIN_PASSWORD)
    return server


"""Get job details of each job that is running on the Jenkins instance"""


def get_job_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    try:
        jenkins = get_server_instance()
        jobs: Generator[Union[Tuple[str, Job], Tuple[Any, Job]], Any, None] = jenkins.get_jobs()
        logger.debug("jobs type is {}".format(type(jobs)))
        for job_name, job_instance in jobs:
            logger.debug('Job Name:%s' % (job_instance.name))
            logger.debug('Job Description:%s' % (job_instance.get_description()))
            logger.debug('Is Job running:%s' % (job_instance.is_running()))
            logger.debug('Is Job enabled:%s' % (job_instance.is_enabled()))
            build_or_none: Optional[Build] = jenkins[job_name].get_last_build_or_none()
            if build_or_none != None:
                build = build_or_none
                get_build_details(build)
        return 200
    except Exception as ex:
        logger.debug("Exception: {0}".format(ex))


def get_build_details(build):
    artifacts = build.get_artifacts()
    # artifact: Artifact
    for artifact in artifacts:
        logger.debug("artifact file name {}".format(artifact.filename))
        logger.debug("artifact data {}".format(artifact.get_data()))
    build_params = build.get_params()
    for job_param in build_params:
        logger.debug("param {}".format(job_param))
    # build.block_until_complete()
    logger.debug("repo url {}".format(build.get_repo_url()))
    build_env_vars = build.get_env_vars()
    for build_env_var in build_env_vars:
        logger.debug("env var {}".format(build_env_var))


def get_plugin_details():
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    for plugin in server.get_plugins().values():
        logger.debug("Short Name:%s" % (plugin.shortName))
        logger.debug("Long Name:%s" % (plugin.longName))
        logger.debug("Version:%s" % (plugin.version))
        logger.debug("URL:%s" % (plugin.url))
        logger.debug("Active:%s" % (plugin.active))
        logger.debug("Enabled:%s" % (plugin.enabled))


def main():
    logger.debug(get_server_instance().version)
    get_job_details()
    get_plugin_details()
    # jenkins_raw()


def jenkins_raw():
    # https://stackoverflow.com/questions/54643387/jenkinsapi-python-how-to-trigger-and-track-the-job-result
    jenkins_url = JENKINS_BASE_URL
    auth = (JENKINS_ADMIN_USER, JENKINS_ADMIN_PASSWORD)
    jenkins_token = constants.JENKINS_TOKEN
    job_name = "simon_job"
    request_url = "{0:s}/buildByToken/buildWithParameters?job={1:s}&token={2:s}".format(
        jenkins_url,
        job_name,
        jenkins_token
    )

# {jenkins_base_url}/buildByToken/buildWithParameters?job={jenkins_deploy_activator_job}&token={jenkins_token}


    logger.debug("Determining next build number")
    job = requests.get(
        "{0:s}/job/{1:s}/api/json".format(
            jenkins_url,
            job_name,
        ),
        auth=auth,
    ).json()
    next_build_number = job['nextBuildNumber']
    next_build_url = "{0:s}/job/{1:s}/{2:d}/api/json".format(
        jenkins_url,
        job_name,
        next_build_number,
    )

    params = {"Foo": "String param 1", "Bar": "String param 2"}
    logger.debug("Triggering build: {0:s} #{1:d}".format(job_name, next_build_number))
    response = requests.post(request_url, data=params, auth=auth)

    response.raise_for_status()
    logger.debug("Job triggered successfully")

    while True:
        print("Querying Job current status...")
        try:
            build_data = requests.get(next_build_url, auth=auth).json()
        except ValueError:
            logger.debug("No data, build still in queue")
            logger.debug("Sleep for 20 sec")
            time.sleep(20)
            continue

        logger.debug("Building: {0}".format(build_data['building']))
        building = build_data['building']
        if building is False:
            break
        else:
            logger.debug("Sleep for 60 sec")
            time.sleep(60)

        logger.debug("Job finished with status: {0:s}".format(build_data['result']))


# def main():  ## Our main method is a little big, but it basically
#     # if (len(sys.argv) == 2):
#     #     blowup()
#     # else:
#     server = connectToJenkins()
#     server.get_credentials()
#     jobs = getJenkinsJobs(server)
#     for job in jobs:
#         print(type(job))
#         print(job)
#         # print(job.name)
#         # print(job.url)
#
#     # jobName = sys.argv[1] + " " + sys.argv[2]  ## builds our job name out of our first 2 arguments.
#     jobName = "Activator Deploy"
#     if (jobs.__contains__(jobName)):  ##make sure the job exists on the server.
#         job = server[jobName]  ##select the job
#         # args = {}
#         # runJenkinsJob(job, sys.argv)  ##run it
#         # runJenkinsJob(job, args)  ##run it
#         job.invoke()
#     else:
#         noJobs()
#

main()  ## run this fella
