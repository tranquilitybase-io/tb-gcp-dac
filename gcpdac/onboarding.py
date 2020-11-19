import json
import tempfile

import git
import yaml
from gcloud import resource_manager

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


def clone_repo_locally(git_details):
    try:
        repo_url = git_details['repoURL']
        with tempfile.TemporaryDirectory() as tmpdirname:
            local_repo = git.Repo.clone_from(repo_url, tmpdirname, no_checkout=True)
            local_repo.git.checkout(git_details['tagName'])
            return local_repo
    except Exception:
        raise Exception("Error cloning repository")


def get_repo_uri(git_details):
    try:
        destination_project = get_destination_project()
        local_repo = clone_repo_locally(git_details)
        create_and_save(local_repo, destination_project)
        gcp_repo = json_builder(destination_project, local_repo)
        payload = json.dumps(str(gcp_repo))
        return {'status': 201, "payload": payload}
    except Exception as ex:
        logger.debug(ex)

    return {'status': 500, "message": "Exception encountered"}


def json_builder(project_id, local_repo):
    url_prefix = "https://source.cloud.google.com/"
    dict_repo = '{"repo_name": "", "project_id": "", "head_link": "", "path_link": "", "browser_link": "", ' \
                '"git_clone": "", "cloud_sdk": ""} '
    dict_repo["repo_name"] = local_repo
    dict_repo["project_id"] = project_id
    dict_repo["head_link"] = url_prefix + project_id + "/" + local_repo + "/+/master:"
    dict_repo["path_link"] = project_id + "/" + local_repo + "/master//"
    dict_repo["browser_link"] = url_prefix + project_id + "/" + local_repo
    dict_repo["git_clone"] = "git clone " + url_prefix + "p/" + project_id + "/r/" + local_repo
    dict_repo["cloud_sdk"] = "gcloud source repos clone " + local_repo + " --project=" + project_id
    return dict_repo