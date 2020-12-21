from google.cloud import storage

from src.main.python.tranquilitybase.gcpdac.configuration.eaglehelper import EagleConfigHelper
from src.main.python.tranquilitybase.gcpdac.configuration.envhelper import EnvHelper
from src.main.python.tranquilitybase.gcpdac.configuration.gcphelper import GcpHelper
from src.main.python.tranquilitybase.gcpdac.configuration.jenkinshelper import JenkinsHelper

global DEFAULT_SHELL
global environment_helper
global eagle_config_helper
global gcp_helper

# TODO: remove these from global scope
global JENKINS_BASE_URL
global JENKINS_USER
global JENKINS_PASSWORD


def init():
    global environment_helper
    environment_helper = EnvHelper()
    establish_eagle_config()
    establish_bash()
    establish_jenkins()
    establish_gcp()


def establish_jenkins():
    global JENKINS_BASE_URL
    global JENKINS_USER
    global JENKINS_PASSWORD

    jenkins_helper = JenkinsHelper()
    JENKINS_BASE_URL = jenkins_helper.jenkins_base_url
    JENKINS_USER = jenkins_helper.jenkins_user
    JENKINS_PASSWORD = jenkins_helper.jenkins_password


def establish_eagle_config():
    global eagle_config_helper
    eagle_config_helper = EagleConfigHelper(environment_helper.get_ec_config_path())


def establish_gcp():
    global gcp_helper
    gcp_helper = GcpHelper()

    if EnvHelper.has_google_credentials():
        global eagle_config_helper
        gcp_project_name = eagle_config_helper.get_gcp_project_name()
        print("GOOGLE_CLOUD_PROJECT: {}".format(gcp_project_name))
        storage.Client(project=gcp_project_name)


def establish_bash():
    global DEFAULT_SHELL
    DEFAULT_SHELL = "/bin/bash"

