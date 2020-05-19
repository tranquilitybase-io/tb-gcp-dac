from python_terraform import Terraform

import config

logger = config.logger

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
    while retry_count < 3:
        logger.debug("Try {}".format(retry_count))
        return_code, stdout, stderr = tf.apply(skip_plan=True, var_file=env_data, capture_output=True)
        logger.debug('Terraform apply return code is {}'.format(return_code))
        logger.debug('Terraform apply stdout is {}'.format(stdout))
        logger.debug("Terraform apply stderr is {}".format(stderr))
        retry_count += 1
        if return_code == 0:
            break
    if return_code == 0:
        code, tf_state, stdout1 = tf.show(json=True)
        tf_outputs = tf.output()
        for output_value in tf_outputs:
            logger.debug('Terraform output value is {}'.format(output_value))
    else:
        tf_state = {}
        tf_outputs = {}
    return {"tf_return_code": return_code, "tf_outputs": tf_outputs, "tf_state": tf_state}

def terraform_destroy(env_data, tf):
    return_code, stdout, stderr = tf.destroy(var_file=env_data, capture_output=True)
    logger.debug('Terraform destroy return code is {}'.format(return_code))
    logger.debug('Terraform destroy stdout is {}'.format(stdout))
    logger.debug('Terraform destroy stderr is {}'.format(stderr))
    return {"tf_return_code": return_code}
