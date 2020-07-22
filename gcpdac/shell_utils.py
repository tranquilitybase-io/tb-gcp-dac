import json
import shlex
import subprocess
from json import JSONDecodeError


def create_repo(repo_name, project_to, project_from):
    call_string = "/bin/bash /app/bash_scripts/create_gcp_repo.sh {repo_name} {project_to} {project_from}".format(
        repo_name=repo_name,
        project_to=project_to,
        project_from=project_from)
    return call_process(call_string)


def copy_repo(source_repo_url, target_gcp_repo_name, project_to, project_from):
    call_string = "/bin/bash /app/bash_scripts/copy_repo_with_history.sh {source_repo_url} {target_gcp_repo_name}  {project_to} {project_from}".format(
        source_repo_url=source_repo_url,
        target_gcp_repo_name=target_gcp_repo_name,
        project_to=project_to,
        project_from=project_from)
    return call_process(call_string)


def delete_repo(repo_name, project_to, project_from):
    call_string = "/bin/bash /app/bash_scripts/delete_gcp_repo.sh {repo_name} {project_to} {project_from}".format(
        repo_name=repo_name,
        project_to=project_to,
        project_from=project_from)
    return call_process(call_string)


def call_jenkins(jenkins_url, jenkins_params: dict):
    for key in jenkins_params:
        value = jenkins_params[key]
        jenkins_url = "{jenkins_url}&{key}={value}".format(jenkins_url=jenkins_url, key=key, value=value)

    call_string = "curl -X POST {}".format(jenkins_url)
    return call_process(call_string)


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


def call_process(call_string):
    command_line_args = shlex.split(call_string)
    subprocess_call = subprocess.Popen(command_line_args, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
    process_output, _ = subprocess_call.communicate()
    returncode = subprocess_call.returncode

    return returncode
