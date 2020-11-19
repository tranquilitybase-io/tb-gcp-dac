import json
import tempfile

import git
import yaml
from gcloud import resource_manager

import config
from gcpdac.shell_utils import create_and_save

logger = config.logger


def get_client():
    return resource_manager.Client()


def list_projects():
    client = get_client()
    for project in client.list_projects():
        print(project)
    return client.list_projects()


def get_ec_config():
    with open('/app/ec-config.yaml', 'rb') as f:
        yaml_variables = yaml.load(f.read())
    return yaml_variables


def get_destination_project():
    project_list = list_projects()
    project_to_prefix = "shared-ec-"
    result = ""
    yaml_variables = get_ec_config()
    tb_discriminator = yaml_variables['tb_discriminator']
    for p in project_list:
        result = p.match(project_to_prefix) + tb_discriminator
    return result


def get_repo_uri(repo_json):
    # json_string = '{"activatorName": "tb-gcp-hpc-activator", "repoURL":"someurl", "tagName": "sometag"}'
    parsed_json = json.loads(repo_json)
    # git clone <repo_url> --branch <tag_name> --single-branch
    with tempfile.TemporaryDirectory() as tmpdirname:
        repo_url = parsed_json['repoURL']
        local_repo = git.Repo.clone_from(repo_url, tmpdirname)
        local_repo.checkout(parsed_json['tagName'])
        copy_to_project_id = get_destination_project()
        flag = create_and_save(local_repo, copy_to_project_id)
        if flag:
            gcp_repo = json_builder(copy_to_project_id, local_repo)
            logger.info("return json : ", gcp_repo)

    return json.dumps(gcp_repo)


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
