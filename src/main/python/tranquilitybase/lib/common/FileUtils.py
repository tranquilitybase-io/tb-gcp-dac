import os
from pathlib import Path
import shutil

from src.main.python.tranquilitybase.gcpdac.configuration.helpers import envhelper
import sys


class FileUtils:

    @staticmethod
    def file_exists(path: str) -> bool:
        file = Path(path)
        if not file.is_file():
            return False
        return True

    @staticmethod
    def dir_exists(path: str) -> bool:
        directory = Path(path)
        if not directory.is_dir():
            return False
        return True\


    @staticmethod
    def delete_path(path: str):
        shutil.rmtree(path, ignore_errors=True)

    @staticmethod
    def get_project_root() -> str:
        if envhelper.EnvHelper.is_ide():
            main = os.path.dirname(sys.modules['__main__'].__file__)
            project_root = os.path.join(main, "../../../../../../")
            project_root = os.path.abspath(project_root)
            return project_root
        return os.path.abspath('/app')

    @staticmethod
    def redirect_path(original: str) -> str:
        return FileUtils.get_project_root() + original

    @staticmethod
    def print_folder_contents():
        print("-- getcwd --")
        cwd = os.getcwd()
        print("Current working directory: {0}".format(cwd))

        print("-- proj root --")
        import pathlib
        currentDirectory = pathlib.Path(FileUtils.get_project_root())
        print(currentDirectory)
        for currentFile in currentDirectory.glob("*"):
            print(currentFile)

        # print("-- recursive root --")
        # import glob
        # currentDirectory = pathlib.Path(FileUtils.get_project_root())
        # for currentpath, folders, files in os.walk(currentDirectory):
        #     for file in files:
        #         print(os.path.join(currentpath, file))
        #
        # print("done", flush=True)