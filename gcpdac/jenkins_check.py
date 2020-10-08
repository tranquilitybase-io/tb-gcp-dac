import config
from gcpdac.jenkins_utils import get_server_instance, get_all_job_details

logger = config.logger

def get_job_details():
    get_all_job_details()
    return 200

def main():
    logger.debug(get_server_instance().version)
#     get_job_details()
#     get_plugin_details()
