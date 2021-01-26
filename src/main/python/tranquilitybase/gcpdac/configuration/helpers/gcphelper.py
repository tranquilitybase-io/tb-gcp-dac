import os

from src.main.python.tranquilitybase.gcpdac.configuration.helpers.envhelper import EnvHelper
from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils


class GcpHelper:
    __gcp_project_name = None

    def __init__(self):
        if EnvHelper.has_google_credentials():
            GcpHelper.__configure_credentials_path()
            GcpHelper.__validate_credentials_file()

    @staticmethod
    def __configure_credentials_path():
        # google_application_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        # print("000000: " + os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        pass

    @staticmethod
    def __validate_credentials_file():
        if not FileUtils.file_exists(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]):
            raise Exception("No file found for GOOGLE_APPLICATION_CREDENTIALS: " + os.environ["GOOGLE_APPLICATION_CREDENTIALS"])


