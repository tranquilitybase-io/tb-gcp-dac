import time

mock_mode = True
terraform_script_root = "/app/src/main/terraform/"


def get_terraform_root() -> str:
    return terraform_script_root


def mock_response():
    time.sleep(30)
    return {"tf_return_code": "0"}
