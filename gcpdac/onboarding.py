import json
import tempfile
import git
import yaml
import config
from gcloud import resource_manager

from gcpdac.path_utils import file_exists
from gcpdac.shell_utils import create_and_save

logger = config.logger


def get_client():
    return resource_manager.Client()


def get_ec_config():
    # TODO: file_path needs a centralised config
    file_path = 'ec-config.yaml'

    if not file_exists(file_path):
        raise Exception("file not found")

    with open(file_path, 'rb') as f:
        yaml_variables = yaml.load(f.read(), yaml.Loader)

    return yaml_variables


def get_destination_project():
    # TODO: project_prefix needs a centralised config
    project_prefix = "shared-ec-"

    yaml_variables = get_ec_config()
    tb_discriminator = yaml_variables['tb_discriminator']
    result = project_prefix + tb_discriminator

    return result


def clone_repo_locally(gitDetails):
    try:
        repo_url = gitDetails['repoURL']
        with tempfile.TemporaryDirectory() as tmpdirname:
            local_repo = git.Repo.clone_from(repo_url, tmpdirname, no_checkout=True)
            local_repo.git.checkout(gitDetails['tagName'])
            return local_repo
    except Exception:
        raise Exception("Error cloning repository")


def get_repo_uri(gitDetails):
    try:
        local_repo = clone_repo_locally(gitDetails)
        create_and_save(local_repo, get_destination_project())
        gcp_repo = {'repository': local_repo}
        payload = json.dumps(str(gcp_repo))
        return payload, 201
    except Exception as ex:
        logger.debug(ex)

    return "Exception encountered", 500
