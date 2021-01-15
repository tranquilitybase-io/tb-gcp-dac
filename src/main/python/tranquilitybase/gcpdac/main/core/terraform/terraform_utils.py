import time

from python_terraform import Terraform
from src.main.python.tranquilitybase.gcpdac.main.core.terraform.terraform_config import mock_mode

# --- Logger ---
import inspect
from src.main.python.tranquilitybase.lib.common.local_logging import *
logger = get_logger(get_frame_name(inspect.currentframe()))


def terraform_init(backend_prefix, terraform_state_bucket, tf: Terraform):
    if mock_mode:
        return

    return_code, stdout, stderr = tf.init(capture_output=True,
                                          backend_config={'bucket': terraform_state_bucket,
                                                          'prefix': backend_prefix})
    logger.debug('Terraform init return code is {}'.format(return_code))
    logger.debug('Terraform init stdout is {}'.format(stdout))
    logger.debug('Terraform init stderr is {}'.format(stderr))


def terraform_apply(env_data, tf: Terraform):
    if mock_mode:
        time.sleep(10)
        return {"tf_return_code": "0", "tf_outputs": "hi", "tf_state": "state"}

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
        #TODO get output for errors
        tf_state = {}
        tf_outputs = {}
    return {"tf_return_code": return_code, "tf_outputs": tf_outputs, "tf_state": tf_state}


def terraform_destroy(env_data, tf):
    if mock_mode:
        time.sleep(10)
        return {"tf_return_code": "0"}

    return_code, stdout, stderr = tf.destroy(var_file=env_data, capture_output=True)
    logger.debug('Terraform destroy return code is {}'.format(return_code))
    logger.debug('Terraform destroy stdout is {}'.format(stdout))
    logger.debug('Terraform destroy stderr is {}'.format(stderr))
    return {"tf_return_code": return_code}