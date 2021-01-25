import os
from pathlib import Path
import shutil


class FileUtils:

    @staticmethod
    def file_exists(path: str) -> bool:
        file = Path(path)
        if not file.is_file():
            return False
        return True

    @staticmethod
    def dir_exists(path: str) -> bool:
        dir = Path(path)
        if not dir.is_dir():
            return False
        return True\


    @staticmethod
    def delete_path(path: str):
        shutil.rmtree(path, ignore_errors=True)

    @staticmethod
    def get_project_root() -> str:
        return os.path.abspath('/app')

    @staticmethod
    def redirect_path(original: str) -> str:
        return FileUtils.get_project_root() + original

