import os
from pathlib import Path

import yaml
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger


class ConfigHelper:
    __gcp_project_name = None

    @staticmethod
    def get_config_file() -> str:
        project_root = os.environ["PROJECT_ROOT"]
        config_yaml_path = project_root + "/config/ec-config.yaml"
        return config_yaml_path

    @staticmethod
    def read_config_map():
        # Returns the EC configuration as a dictionary
        logger = get_logger('ConfigHelper')

        try:
            file_path = ConfigHelper.get_config_file()
            with open(file_path, 'r') as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    logger.exception("Failed to parse EC YAML after successfully opening - {}".format(exc))
                    raise
        except Exception:
            logger.exception("Failed to load EC YAML file")
            raise

    def __init__(self):
        self.__validate_config_file()
        self.__parse_config_file()

    def __validate_config_file(self):
        file_path = ConfigHelper.get_config_file()
        file = Path(file_path)
        if not file.is_file():
            raise Exception("No file found for " + file_path)

    def __parse_config_file(self):
        file_path = ConfigHelper.get_config_file()
        with open(file_path) as f:
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
