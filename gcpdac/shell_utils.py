import shlex
import subprocess

import config

logger = config.logger

# TODO pass this in through config file in docker/kubernetes
jenkins_server = "TODO"


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


def call_jenkins(git_repo_url):
    logger.info("Calling Jenkins TODO IMPLEMENT")
    # call_string = "curl http://{jenkins_server}/jenkins/git/notifyCommit?url={git_repo_url}".format(
    # git_repo_url=git_repo_url,
    # jenkins_server=jenkins_server)
    # TODO this is a hard-coded jenkins server! just for demo, remove soon after
    # call_string = "curl -X POST http://remote_user:11eccd7308d0e2f408e53f04b16c839e65@34.105.172.132:8080/job/Activator%20Deploy/build?token=11eccd7308d0e2f408e53f04b16c839e65"
    # call_process(call_string)


def call_process(call_string):
    logger.debug("Process executed: {}".format(call_string))
    command_line_args = shlex.split(call_string)
    subprocess_call = subprocess.Popen(command_line_args, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, universal_newlines=True)
    process_output, _ = subprocess_call.communicate()
    logger.debug("Process output: {}".format(process_output))
