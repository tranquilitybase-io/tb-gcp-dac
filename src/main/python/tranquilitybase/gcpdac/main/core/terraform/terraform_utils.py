import time
import traceback
from python_terraform import Terraform

from src.main.python.tranquilitybase.gcpdac.configuration.helpers.eaglehelper import EagleConfigHelper
from src.main.python.tranquilitybase.gcpdac.main.core.terraform.terraform_config import get_terraform_path

# --- Logger ---
import inspect

from src.main.python.tranquilitybase.lib.common.StringUtils import is_none_or_empty
from src.main.python.tranquilitybase.lib.common.local_logging import get_logger, get_frame_name

logger = get_logger(get_frame_name(inspect.currentframe()))


def validate_terraform_path():
    terraform_source_path = get_terraform_path('folder_creation')
    tf = Terraform(working_dir=terraform_source_path)
    terraform_plan(tf)


def validate_terraform_config():
    ec_config = EagleConfigHelper.config_dict

    terraform_state_bucket = ec_config['terraform_state_bucket']
    tb_discriminator = ec_config['tb_discriminator']
    if is_none_or_empty(terraform_state_bucket) or \
            is_none_or_empty(tb_discriminator):
        raise Exception("terraform value from ec_config found to be invalid")


def terraform_plan(tf: Terraform):

    return_code, stdout, stderr = tf.plan(capture_output=True)
    logger.debug('Terraform plan return code is {}'.format(return_code))
    logger.debug('Terraform plan stdout is {}'.format(stdout))
    logger.debug('Terraform plan stderr is {}'.format(stderr))


def terraform_init(backend_prefix, terraform_state_bucket, tf: Terraform):

    return_code, stdout, stderr = tf.init(capture_output=True,
                                          backend_config={'bucket': terraform_state_bucket,
                                                          'prefix': backend_prefix})
    logger.debug('Terraform init return code is {}'.format(return_code))
    logger.debug('Terraform init stdout is {}'.format(stdout))
    logger.debug('Terraform init stderr is {}'.format(stderr))


def terraform_apply(env_data, tf: Terraform):

    retry_count = 0
    return_code = 0
    while retry_count < 5:
        logger.debug("Try {}".format(retry_count))
        return_code, stdout, stderr = tf.apply(skip_plan=True, var_file=env_data, capture_output=True)
        logger.debug('Terraform apply return code is {}'.format(return_code))
        logger.debug('Terraform apply stdout is {}'.format(stdout))
        logger.debug("Terraform apply stderr is {}".format(stderr))
        retry_count += 1
        if return_code == 0:
            break
        time.sleep(30)

    if return_code == 0:
        show_return_code, tf_state, stdout = tf.show(json=True)
        logger.debug('Terraform show return code is {}'.format(show_return_code))
        logger.debug('Terraform show stdout is {}'.format(stdout))
        tf_outputs = tf.output()
        for output_value in tf_outputs:
            logger.debug('Terraform output value is {}'.format(output_value))
    else:
        # TODO get output for errors
        tf_state = {}
        tf_outputs = {}
        traceback.print_stack()
    return {"tf_return_code": return_code, "tf_outputs": tf_outputs, "tf_state": tf_state}


def terraform_destroy(env_data, tf):

    return_code, stdout, stderr = tf.destroy(var_file=env_data, capture_output=True)
    logger.debug('Terraform destroy return code is {}'.format(return_code))
    logger.debug('Terraform destroy stdout is {}'.format(stdout))
    logger.debug('Terraform destroy stderr is {}'.format(stderr))
    return {"tf_return_code": return_code}
