import os
import time

from src.main.python.tranquilitybase.lib.common.FileUtils import FileUtils

mock_mode = False
terraform_script_root = "/app/src/main/terraform"


def get_terraform_root() -> str:
    return os.path.join(FileUtils.get_project_root(), terraform_script_root)


def get_terraform_path(path: str) -> str:
    return os.path.join(get_terraform_root(), path)


def mock_response():
    time.sleep(30)
    return {"tf_return_code": "0"}


