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
        tf_state = terraform_show(tf)
    else:
        tf_state = {}
    return {"tf_return_code": return_code, "tf_state": tf_state}


def terraform_show(tf: Terraform):
    return_code, tf_state, stdout = tf.show(json=True)
    output_values = tf.output()
    logger.debug('Terraform output values is {}'.format(output_values))
    for output_value in output_values:
        logger.debug('Terraform output value is {}'.format(output_value))
    logger.debug('Terraform state is {}'.format(tf_state))
    logger.debug('Terraform show return code is {}'.format(return_code))
    logger.debug('Terraform show stdout is {}'.format(stdout))
    return tf_state

def terraform_output(tf: Terraform, output_value_key):
    return tf.output(output_value_key)


def terraform_destroy(env_data, tf):
    return_code, stdout, stderr = tf.destroy(var_file=env_data, capture_output=False)
    logger.debug('Terraform destroy return code is {}'.format(return_code))
    logger.debug('Terraform destroy stdout is {}'.format(stdout))
    logger.debug('Terraform destroy stderr is {}'.format(stderr))
    return {"tf_return_code": return_code}

