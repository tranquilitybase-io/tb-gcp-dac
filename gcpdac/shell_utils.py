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


def delete_repo(repo_name, project_to, project_from):
    logger.info("Deleting repo {repo_name} in project {project_to}".format(repo_name=repo_name, project_to=project_to))
    call_string = "/bin/bash /app/bash_scripts/delete_gcp_repo.sh {repo_name} {project_to} {project_from}".format(
        repo_name=repo_name,
        project_to=project_to,
        project_from=project_from)
    call_process(call_string)


def call_process(call_string):
    logger.debug("call string is {}".format(call_string))
    command_line_args = shlex.split(call_string)
    subprocess_call = subprocess.Popen(command_line_args, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
    process_output, _ = subprocess_call.communicate()
    logger.debug("Process output is {}".format(process_output))
    # logger.debug("response code is {}".format(subprocess_call))
