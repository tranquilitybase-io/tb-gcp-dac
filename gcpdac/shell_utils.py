import shlex
import subprocess

import config

logger = config.logger

def create_repo(repo_name, project_to, project_from):
    logger.info("Creating repo {repo_name} in project {project_to}".format(repo_name=repo_name, project_to=project_to))
    call_string = "/bin/bash /app/bash_scripts/create_gcp_repo.sh {repo_name} {project_to} {project_from}".format(
        repo_name=repo_name,
        project_to=project_to,
        project_from=project_from)
    call_process(call_string)


def copy_repo(source_repo_url, target_gcp_repo_name, project_to, project_from):
    logger.info(
        "Copying source repo {source_repo_url} to target gcp repo {target_gcp_repo_name} in project {project_to}".format(
            source_repo_url=source_repo_url, target_gcp_repo_name=target_gcp_repo_name, project_to=project_to))
    call_string = "/bin/bash /app/bash_scripts/copy_repo_with_history.sh {source_repo_url} {target_gcp_repo_name}  {project_to} {project_from}".format(
        source_repo_url=source_repo_url,
        target_gcp_repo_name=target_gcp_repo_name,
        project_to=project_to,
        project_from=project_from)
    call_process(call_string)


def delete_repo(repo_name, project_to, project_from):
    logger.info("Deleting repo {repo_name} in project {project_to}".format(repo_name=repo_name, project_to=project_to))
    call_string = "/bin/bash /app/bash_scripts/delete_gcp_repo.sh {repo_name} {project_to} {project_from}".format(
        repo_name=repo_name,
        project_to=project_to,
        project_from=project_from)
    call_process(call_string)


def call_jenkins(git_repo_url, deployment_environment, deployment_project_id):
    logger.info("Calling Jenkins TODO IMPLEMENT")
    logger.info("Git Repo URL {}".format(git_repo_url))
    logger.info("Deployment Environment {}".format(deployment_environment))
    logger.info("Deployment Project ID {}".format(deployment_project_id))

    jenkins_server = config.JENKINS_URL
    logger.info("Jenkins URL = {}".format(jenkins_server))
    call_string = "curl -X POST {}".format(jenkins_server)
    call_process(call_string)


def call_process(call_string):
    logger.debug("Process executed: {}".format(call_string))
    command_line_args = shlex.split(call_string)
    subprocess_call = subprocess.Popen(command_line_args, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, universal_newlines=True)
    process_output, _ = subprocess_call.communicate()
    logger.debug("Process output: {}".format(process_output))
    returncode = subprocess_call.returncode
    logger.debug("Return code: {}".format(returncode))

    return returncode
