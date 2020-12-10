import os


class EnvHelper:

    absolute_ec_config_path = None
    absolute_gcp_credentials_path = None

    def __init__(self, validate: bool = True):
        self.__consider_config()
        if validate:
            self.__validate_config()

    def is_ide(self):
        return os.getenv('IS_IDE')

    def __consider_config(self):

        if self.is_ide():
            print("== IS IDE ==")
            os.environ["DEBUG"] = "true"

            os.environ["DAC_JENKINS_USER"] = "not set"
            os.environ["DAC_JENKINS_PASSWORD"] = "not set"
            os.environ["JENKINS_BASE_URL"] = "not set"

            # os.environ["CELERY_BROKER_URL"] = "not set"
            # os.environ["CELERY_RESULT_BACKEND"] = "not set"

            os.environ["EC_CONFIG"] = "/resources/main/config/ec-config.yaml"
            EnvHelper.absolute_ec_config_path = os.environ["PROJECT_ROOT"] + os.environ["EC_CONFIG"]

            relative_gcp_credentials_path = "/credentials/credentials.json"
            EnvHelper.absolute_gcp_credentials_path = os.environ["PROJECT_ROOT"] + relative_gcp_credentials_path
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = EnvHelper.absolute_gcp_credentials_path

            if not os.getenv("APP_PORT"):
                os.environ["APP_PORT"] = "3100"
        else:
            print("== NOT IDE ==")

    def __validate_config(self):
        EnvHelper.validate_environ("DEBUG")

        EnvHelper.validate_environ("JENKINS_BASE_URL")
        EnvHelper.validate_environ("DAC_JENKINS_USER")
        EnvHelper.validate_environ("DAC_JENKINS_PASSWORD")

        # EnvHelper.validate_environ("CELERY_BROKER_URL")
        # EnvHelper.validate_environ("CELERY_RESULT_BACKEND")

        EnvHelper.validate_environ("EC_CONFIG")
        EnvHelper.validate_environ("GOOGLE_APPLICATION_CREDENTIALS")

        EnvHelper.validate_environ("APP_PORT")

    @staticmethod
    def validate_environ(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise Exception("Required environmental variable: {0} not found.".format(name))
        return value

    #
    # =========
    def get_app_port(self):
        return os.getenv("APP_PORT")

    def get_ec_config_path(self):
        return EnvHelper.absolute_ec_config_path

    def get_debug_state(self):
        return os.getenv("DEBUG")

    def get_celery_result_backend(self):
        return os.getenv("CELERY_RESULT_BACKEND")

    def get_celery_broker_url(self):
        return os.getenv("CELERY_BROKER_URL")
