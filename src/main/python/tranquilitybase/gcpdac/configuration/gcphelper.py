import os
import yaml
from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils


class GcpHelper:
    __gcp_project_name = None
    __ec_file_path_from_project_root = None

    def __init__(self, ec_file_path: str):
        self.__configure_credentials_path()
        self.__validate_credentials_file()

        GcpHelper.__ec_file_path_from_project_root = GcpHelper.redirect_path(ec_file_path)
        self.__validate_config_file()
        self.__parse_config_file()

    def __configure_credentials_path(self):
        google_application_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        google_application_credentials = GcpHelper.redirect_path(google_application_credentials)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_application_credentials

    def __validate_credentials_file(self):
        if not FileUtils.file_exists(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]):
            raise Exception("No file found for GOOGLE_APPLICATION_CREDENTIALS: " + os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

    def __validate_config_file(self):
        if not FileUtils.file_exists(GcpHelper.__ec_file_path_from_project_root):
            raise Exception("No file found for " + GcpHelper.__ec_file_path_from_project_root)

    def __parse_config_file(self):
        with open(GcpHelper.__ec_file_path_from_project_root) as f:
            try:
                data: dict = yaml.safe_load(f)
                self.__gcp_project_name = data.get("ec_project_name")
            except yaml.YAMLError as exc:
                raise SystemError("Failed to parse EC YAML after successfully opening - {}".format(exc))

    def get_gcp_project_name(self) -> str:
        if not self.__gcp_project_name:
            raise ValueError("No GOOGLE_CLOUD_PROJECT set for Flask application")
        return self.__gcp_project_name

    @staticmethod
    def redirect_path(original: str) -> str:
        return FileUtils.get_project_root() + original
