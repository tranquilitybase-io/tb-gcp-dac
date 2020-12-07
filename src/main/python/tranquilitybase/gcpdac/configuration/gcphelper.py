import os
import yaml
from pathlib import Path


class GcpHelper:
    __gcp_project_name = None

    def __init__(self, ec_file_path: str):
        self.__validate_config_file(ec_file_path)
        self.__parse_config_file(ec_file_path)

    def __validate_config_file(self, ec_file_path: str):
        file = Path(ec_file_path)
        if not file.is_file():
            raise Exception("No file found for " + ec_file_path)

    def __parse_config_file(self, ec_file_path: str):
        with open(ec_file_path) as f:
            try:
                data: dict = yaml.safe_load(f)
                self.__gcp_project_name = data.get("ec_project_name")
                print(self.__gcp_project_name)
            except yaml.YAMLError as exc:
                raise SystemError("Failed to parse EC YAML after successfully opening - {}".format(exc))

    def get_gcp_project_name(self) -> str:
        if not self.__gcp_project_name:
            raise ValueError("No GOOGLE_CLOUD_PROJECT set for Flask application")
        return self.__gcp_project_name
