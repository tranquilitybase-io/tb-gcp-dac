import os
import yaml

from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils


class EagleConfigHelper:
    __ec_file_path_from_project_root = None
    __gcp_project_name = None
    config_dict = None

    def __init__(self, ec_file_path: str):
        EagleConfigHelper.__ec_file_path_from_project_root = FileUtils.redirect_path(ec_file_path)
        # self.__validate_config_file()
        self.__parse_config_file()

    def __validate_config_file(self):
        print("-- proj root --")
        import pathlib
        currentDirectory = pathlib.Path(FileUtils.get_project_root())
        print(currentDirectory)
        for currentFile in currentDirectory.glob("*"):
            print(currentFile)

        print("-- src --")
        currentDirectory = pathlib.Path(FileUtils.get_project_root()+"/src/")
        print(currentDirectory)
        for currentFile in currentDirectory.glob("*"):
            print(currentFile)


        print("-- recursive --")
        import glob
        currentDirectory = pathlib.Path(FileUtils.get_project_root()+"/resources/")
        for currentpath, folders, files in os.walk(currentDirectory):
            for file in files:
                print(os.path.join(currentpath, file))

        print("done", flush=True)


        print("-- resources --")
        currentDirectory = pathlib.Path(FileUtils.get_project_root()+"/resources/")
        print(currentDirectory)
        for currentFile in currentDirectory.glob("*"):
            print(currentFile)
        print("----", flush=True)
        print("EagleConfigHelper.__ec_file_path_from_project_root: " + EagleConfigHelper.__ec_file_path_from_project_root, flush=True)

        with open(EagleConfigHelper.__ec_file_path_from_project_root, 'r') as viewFileOpen:
            data = viewFileOpen.read()
        print(data, flush=True)

        currentDirectory = pathlib.Path(EagleConfigHelper.__ec_file_path_from_project_root)
        if not FileUtils.file_exists(currentDirectory):
            raise Exception("No file found for " + EagleConfigHelper.__ec_file_path_from_project_root)

    def __parse_config_file(self):
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


