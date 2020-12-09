import os
from src.main.python.tranquilitybase.gcpdac.core.exceptions import DacJenkinsError
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger


class JenkinsHelper:
    jenkins_base_url = None
    jenkins_user = None
    jenkins_password = None

    logger = get_logger('JenkinsHelper')

    def __init__(self):
        self.__set_jenkins_config()

    def __set_jenkins_config(self):
        try:
            self.jenkins_base_url = "http://" + os.environ['JENKINS_BASE_URL']
            self.jenkins_user = os.environ['DAC_JENKINS_USER']
            self.jenkins_password = os.environ['DAC_JENKINS_PASSWORD']

        except Exception as ex:
            self.logger.exception(ex)
            raise DacJenkinsError(
                "Jenkins environment variables not set. Check JENKINS_BASE_URL are set")
