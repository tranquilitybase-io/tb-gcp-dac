import os
import yaml

from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils


class EagleConfigHelper:
    __ec_file_path_from_project_root = None
    __gcp_project_name = None
    config_dict = None

    def __init__(self, ec_file_path: str):
        EagleConfigHelper.__ec_file_path_from_project_root = FileUtils.redirect_path(ec_file_path)
        self.__validate_config_file()
        self.__parse_config_file()

    def __validate_config_file(self):
        if not FileUtils.file_exists(EagleConfigHelper.__ec_file_path_from_project_root):

            import glob
            print("-- proj root --")
            print(glob.glob(FileUtils.get_project_root()))
            print("----", flush=True)
            
            raise Exception("No file found for " + EagleConfigHelper.__ec_file_path_from_project_root)

    def __parse_config_file(self):
        with open(EagleConfigHelper.__ec_file_path_from_project_root) as f:
            try:
                EagleConfigHelper.config_dict: dict = yaml.safe_load(f)
                EagleConfigHelper.__gcp_project_name = EagleConfigHelper.config_dict.get("ec_project_name")
            except yaml.YAMLError as exc:
                raise SystemError("Failed to parse EC YAML after successfully opening - {}".format(exc))

    @staticmethod
    def get_gcp_project_name() -> str:
        if not EagleConfigHelper.__gcp_project_name:
            raise ValueError("'ec_project_name' not set in eagle console config (default: ec-config.yaml)")
        return EagleConfigHelper.__gcp_project_name


