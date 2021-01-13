import os
from pathlib import Path


class FileUtils:

    @staticmethod
    def file_exists(path: str) -> bool:
        file = Path(path)
        if not file.is_file():
            return False
        return True

    @staticmethod
    def get_project_root(containerBuild: bool = True) -> str:
        if not containerBuild:
            # TODO: something better
            return os.path.normpath('../../../../../../')
        return os.path.abspath('/app')

    @staticmethod
    def redirect_path(original: str) -> str:
        return FileUtils.get_project_root() + original
