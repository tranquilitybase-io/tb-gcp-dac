import json
import os

import yaml
from gcloud import resource_manager
from git import RemoteProgress, Repo

import config
from gcpdac.path_utils import file_exists
from gcpdac.shell_utils import create_and_save

logger = config.logger


def get_client():
    return resource_manager.Client()


def get_ec_config():
    file_path = 'ec-config.yaml'
    if not file_exists(file_path):
        raise Exception("file not found")

    with open(file_path, 'rb') as f:
        yaml_variables = yaml.load(f.read(), yaml.Loader)

    return yaml_variables


def get_destination_project():
    project_prefix = "shared-ec-"
    yaml_variables = get_ec_config()
    tb_discriminator = yaml_variables['tb_discriminator']
    return project_prefix + tb_discriminator


def clone_repo_locally(gitDetails):
    try:
        dirname = os.getcwd() + "/temp_repo"
        cloned_repo = Repo.clone_from(gitDetails['repo']['url'], dirname, progress=CloneProgress())
        logger.info("Change repo - %s", str(cloned_repo))
        return dirname
    except Exception as e:
        logger.exception("Error cloning repository {}", e.__traceback__)
        raise Exception("Error cloning repository")


def get_repo_uri(gitDetails):
    try:
        destination_project = get_destination_project()
        local_repo = str(clone_repo_locally(gitDetails))
        logger.debug("Cloning %s to local - %s ", gitDetails['repo']['url'], local_repo)
        gcp_repo_name = gitDetails['repo']['name']
        run(create_and_save(local_repo, destination_project, gcp_repo_name))
        gcp_clone_response = json_builder(destination_project, gcp_repo_name)
        payload = json.dumps(gcp_clone_response)
        return payload, 202
    except Exception as ex:
        logger.exception(ex.__traceback__)
    return "Exception encountered", 501


def run(create_and_save):
    try:
        create_and_save.send(None)
    except StopIteration as e:
        return e.value


def json_builder(project_id, local_repo):
    url_prefix = "https://source.developers.google.com/"
    return {"repo_name": local_repo,
            "project_id": project_id,
            "head_link": url_prefix + project_id + "/" + local_repo + "/+/master:",
            "path_link": project_id + "/" + local_repo + "/master//",
            "browser_link": url_prefix + project_id + "/" + local_repo,
            "git_clone": "git clone " + url_prefix + "p/" + project_id + "/r/" + local_repo,
            "git_clone_url": url_prefix + "p/" + project_id + "/r/" + local_repo,
            "cloud_sdk": "gcloud source repos clone " + local_repo + " --project=" + project_id}


class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)
