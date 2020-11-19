import json

import yaml
from gcloud import resource_manager

import config

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


# always return True
def get_repo_uri(repo_json):
    json_string = '{"activatorName": "tb-gcp-activator-name", "repoURL":"someurl", "tagName": "sometag"}'
    parsed_json = json.loads(json_string)
    gcp_repo = '{"repository": "https://source.developers.google.com/p/shared-ec-xxxxxx/r/tb-gcp-activator-name"}'
    # git clone <repo_url> --branch <tag_name> --single-branch
    # with tempfile.TemporaryDirectory() as tmpdirname:
    #     repo_url = parsed_json['repoURL']
    #     local_repo = git.Repo.clone_from(repo_url, tmpdirname)
    #     local_repo.checkout(parsed_json['tagName'])
    #     flag = create_and_save(local_repo, get_destination_project())
    #     if flag:
    #         gcp_repo["repository"] = local_repo
    #         logger.info("return json : ", gcp_repo)

    return json.dumps(gcp_repo)