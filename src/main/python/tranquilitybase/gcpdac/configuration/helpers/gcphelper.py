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
        if EnvHelper.is_ide():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = FileUtils.redirect_path(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
            print("GOOGLE_APPLICATION_CREDENTIALS redirect_path: " + os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

    @staticmethod
    def __validate_credentials_file():
        cred_file = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        if not FileUtils.file_exists(cred_file):
            raise Exception("No file found for GOOGLE_APPLICATION_CREDENTIALS: " + cred_file)


