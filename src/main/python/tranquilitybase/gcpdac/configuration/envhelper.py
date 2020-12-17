import os
from enum import Enum


class Environments(Enum):
    IDE = 1
    CONTAINER = 2


class EnvHelper:

    environment: Environments = None
    has_run_previously = False

    def __init__(self, validate: bool = True):
        if EnvHelper.has_run_previously:
            raise Exception("EnvHelper has already been initialised")

        EnvHelper.hasRun = True

        self.__consider_config()
        if validate:
            self.__validate_config()
            EnvHelper.print_config()
        else:
            # Used for unit tests
            pass

    @staticmethod
    def is_ide() -> bool:
        return os.getenv('IS_IDE')

    @staticmethod
    def has_google_credentials() -> bool:
        return os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    @classmethod
    def print_env(cls, name: str, redact: bool = False):
        if not redact:
            print("Env {0}: {1}".format(name, os.environ[name]))
        else:
            print("Env {0}: {1}".format(name, "****"))

    @classmethod
    def print_config(self):
        print("")
        print("====================")
        print("====== Config ======")
        print("====================")
        print("")
        print("Environment: " + EnvHelper.environment.name)
        print("")
        EnvHelper.print_env("DEBUG")
        EnvHelper.print_env("APP_PORT")
        EnvHelper.print_env("DAC_JENKINS_USER")
        EnvHelper.print_env("DAC_JENKINS_PASSWORD", True)
        EnvHelper.print_env("JENKINS_BASE_URL")
        EnvHelper.print_env("CELERY_BROKER_URL")
        EnvHelper.print_env("CELERY_RESULT_BACKEND")
        EnvHelper.print_env("EC_CONFIG")
        if EnvHelper.has_google_credentials():
            EnvHelper.print_env("GOOGLE_APPLICATION_CREDENTIALS")
        else:
            print("GOOGLE_APPLICATION_CREDENTIALS are not set - GCP functionality disabled")
        print("")
        print("====================")
        print("", flush=True)

    def __consider_config(self):

        if EnvHelper.is_ide():
            EnvHelper.environment = Environments.IDE
            os.environ["DEBUG"] = "true"

            os.environ["DAC_JENKINS_USER"] = "not set"
            os.environ["DAC_JENKINS_PASSWORD"] = "not set"
            os.environ["JENKINS_BASE_URL"] = "not set"

            os.environ["CELERY_BROKER_URL"] = "not set"
            os.environ["CELERY_RESULT_BACKEND"] = "not set"

            os.environ["EC_CONFIG"] = "/resources/main/config/ec-config.yaml"
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/credentials/credentials.json"

            if not os.getenv("APP_PORT"):
                os.environ["APP_PORT"] = "3100"

        else:
            EnvHelper.environment = Environments.CONTAINER

    def __validate_config(self):
        EnvHelper.validate_environ("DEBUG")

        EnvHelper.validate_environ("JENKINS_BASE_URL")
        EnvHelper.validate_environ("DAC_JENKINS_USER")
        EnvHelper.validate_environ("DAC_JENKINS_PASSWORD")

        EnvHelper.validate_environ("CELERY_BROKER_URL")
        EnvHelper.validate_environ("CELERY_RESULT_BACKEND")

        EnvHelper.absolute_ec_config_path = EnvHelper.validate_environ("EC_CONFIG")

        EnvHelper.validate_environ("APP_PORT")

    @staticmethod
    def validate_environ(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise Exception("Required environmental variable: {0} not found.".format(name))
        return value

    #
    # =========
    def get_app_port(self) -> str:
        return os.getenv("APP_PORT")

    def get_ec_config_path(self) -> str:
        return os.getenv("EC_CONFIG")

    def get_debug_state(self) -> str:
        return os.getenv("DEBUG")

    def get_celery_result_backend(self) -> str:
        return os.getenv("CELERY_RESULT_BACKEND")

    def get_celery_broker_url(self) -> str:
        return os.getenv("CELERY_BROKER_URL")


