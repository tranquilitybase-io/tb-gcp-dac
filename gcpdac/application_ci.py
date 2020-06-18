import config
from gcpdac.shell_utils import call_jenkins

logger = config.logger


def create_application(applicationdata):
    # create terraform vars file
    # check vars file into repo
    # check repo for result file created by Jenkins CI

    # OR

    # create terraform vars file

    # ec_config = config.read_config_map()
    # TODO get jenkins url from ec_config ??

    application_id = applicationdata.get("id")
    logger.debug("application is %s", application_id)
    application_name = applicationdata.get("name")
    git_repo_url = applicationdata.get("activatorGitUrl")
    # call Jenkins CI directly with vars file
    call_jenkins(git_repo_url)

    # TODO add check of jenkins result

    return {"return_code": 0}


def delete_application(applicationdata):
    # TODO place holder to call Jenkins

    return {"return_code": 0}
