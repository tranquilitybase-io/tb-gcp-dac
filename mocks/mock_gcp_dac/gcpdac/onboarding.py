import json

import yaml
from gcloud import resource_manager
from gcpdac.onboarding import json_builder

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


def get_repo_uri(repo_json):
    logger.debug("json - %s", repo_json)
    response = json_builder("project_id_mock", "local_repo_mock")
    return json.dumps(response)
