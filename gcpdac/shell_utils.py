import shlex
import subprocess
import config

logger = config.logger


def create_repo(repo_name, project_to, project_from):
    logger.info("Creating repo {repo_name} in project {project_to}".format(repo_name=repo_name, project_to=project_to))
    call_string = "./bash_scripts/create_gcp_repo.sh {repo_name} {project_to} {project_from}".format(repo_name=repo_name,
                                                                                                  project_to=project_to,
                                                                                                  project_from=project_from)
    logger.debug("call string is {}".format(call_string))
    subprocess_call = subprocess.call(shlex.split(call_string))
    logger.debug("response code is {}".format(subprocess_call))
    return subprocess_call
