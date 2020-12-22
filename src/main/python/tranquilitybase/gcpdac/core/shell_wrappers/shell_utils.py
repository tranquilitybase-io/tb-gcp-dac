import json
import shlex
import subprocess
from asyncio import coroutine
from json import JSONDecodeError

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))

bash_scripts_root = "/app/src/main/bash/tranquilitybase/gcpdac/bash_scripts/"


def create_repo(repo_name, project_to, project_from):
    call_string = "/bin/bash {bash_scripts_root}create_gcp_repo.sh {repo_name} {project_to} {project_from}".format(
        bash_scripts_root=bash_scripts_root,
        repo_name=repo_name,
        project_to=project_to,
        project_from=project_from)
    return call_process(call_string, shell=True)


def copy_repo(source_repo_url, target_gcp_repo_name, project_to, project_from):
    call_string = "/bin/bash {bash_scripts_root}copy_repo_with_history.sh {source_repo_url} {target_gcp_repo_name}  {project_to} {project_from}".format(
        bash_scripts_root=bash_scripts_root,
        source_repo_url=source_repo_url,
        target_gcp_repo_name=target_gcp_repo_name,
        project_to=project_to,
        project_from=project_from)
    return call_process(call_string, shell=True)


def delete_repo(repo_name, project_to, project_from):
    call_string = "/bin/bash {bash_scripts_root}delete_gcp_repo.sh {repo_name} {project_to} {project_from}".format(
        bash_scripts_root=bash_scripts_root,
        repo_name=repo_name,
        project_to=project_to,
        project_from=project_from)
    return call_process(call_string, shell=True)


async def create_and_save(local_git_repo, project_to, remote_repo):
    call_string = "/bin/bash {bash_scripts_root}create_save_onboarding_repo.sh {local_git_repo} {project_to} {remote_repo}".format(
        bash_scripts_root=bash_scripts_root,
        local_git_repo=local_git_repo,
        project_to=project_to,
        remote_repo=remote_repo)
    return call_process(call_string, shell=False, debug=True)


# Add access to given users from bottom_level_folder_id to top_level_folder_id
def add_access_to_folders(bottom_level_folder_id, users, top_level_folder_id):
    print("add_access_to_folders {},{},{}".format(bottom_level_folder_id, users, top_level_folder_id))
    top_level_folder_id = str(top_level_folder_id).replace("folders/", "")
    parent_folder_id = get_parent_folder_id(bottom_level_folder_id)
    while not (parent_folder_id == '' or parent_folder_id == top_level_folder_id):
        for team_member in users:
            assign_user_to_folder(team_member, parent_folder_id)
        parent_folder_id = get_parent_folder_id(parent_folder_id)


def assign_user_to_folder(user, folder):
    print("assign_member {},{}".format(user, folder))
    command = "gcloud resource-manager folders add-iam-policy-binding {folder} --member='user:{user}' --role='roles/viewer'".format(
        folder=folder, user=user)
    process_output = subprocess.run(shlex.split(command), capture_output=True, shell=True)
    print(process_output)


def get_parent_folder_id(folder_id):
    print("get_parent_folder_id {}".format(folder_id))
    command = "gcloud resource-manager folders describe %s --format=json" % folder_id
    process_output = subprocess.run(shlex.split(command), capture_output=True, shell=True)
    print(process_output.stdout)
    json_response = {}
    try:
        json_response = json.loads(process_output.stdout)
    except JSONDecodeError as e:
        print(e)

    parent_folder_id = json_response.get('parent', '').replace('folders/', '')
    print("parent_folder_id {}".format(parent_folder_id))
    return parent_folder_id


def consider_process_debug(subprocess_call, shell, call_string: str, logging: bool):
    if not logging:
        return

    if shell:
        logger.warn("shell output will not be presented to the docker logs for CMD: " + call_string)
        process_output, _ = subprocess_call.communicate()
        logger.debug(logger)
    else:
        logger.debug("stdout from " + call_string)
        while True:
            line = subprocess_call.stdout.readline()
            if not line:
                break
            logger.debug(line.rstrip())

        logger.debug("stdout end")


def call_process(call_string, shell, debug=True):
    try:
        command_line_args = shlex.split(call_string)
        subprocess_call = subprocess.Popen(command_line_args, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, universal_newlines=True, shell=shell)

        consider_process_debug(subprocess_call, shell, call_string, debug)
        return subprocess_call.returncode

    except Exception as ex:
        logger.debug("Error running CMD: " + call_string)
        logger.debug(ex)
        return 1
