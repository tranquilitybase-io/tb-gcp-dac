import yaml
import pathlib

from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils


class EagleConfigHelper:
    __ec_file_path_from_project_root = None
    __gcp_project_name = None
    config_dict = None

    def __init__(self, ec_file_path: str):
        EagleConfigHelper.__ec_file_path_from_project_root = FileUtils.redirect_path(ec_file_path)
        EagleConfigHelper.validate_config_file()
        EagleConfigHelper.parse_config_file()

    @staticmethod
    def validate_config_file():
        current_directory = pathlib.Path(EagleConfigHelper.__ec_file_path_from_project_root)
        if not FileUtils.file_exists(current_directory):
            raise Exception("No file found for " + EagleConfigHelper.__ec_file_path_from_project_root)

    @staticmethod
    def parse_config_file():
        with open(EagleConfigHelper.__ec_file_path_from_project_root) as f:
            try:
                EagleConfigHelper.config_dict: dict = yaml.safe_load(f)
                EagleConfigHelper.__gcp_project_name = EagleConfigHelper.config_dict.get("ec_project_name")
            except yaml.YAMLError as exc:
                print("path: " + EagleConfigHelper.__ec_file_path_from_project_root)
                raise SystemError("Failed to parse EC YAML after successfully opening - {}".format(exc))

    @staticmethod
    def get_gcp_project_name() -> str:
        if not EagleConfigHelper.__gcp_project_name:
            raise ValueError("'ec_project_name' not set in eagle console config (default: ec-config.yaml)")
        return EagleConfigHelper.__gcp_project_name


