import os


def file_exists(param: str):
    return os.path.isfile(param)
