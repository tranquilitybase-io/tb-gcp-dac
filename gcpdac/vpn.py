# Supports all actions concerning VPN
import json
from pprint import pformat

from celery import states
from celery.result import AsyncResult
from flask import abort

import config
from gcpdac.celery_tasks import create_vpn_task, delete_vpn_task
from gcpdac.utils import remove_keys_from_dict
from gcpdac.vpn_terraform import create_vpn, delete_vpn

logger = config.logger


def create(vpnDetails):
    logger.debug(pformat(vpnDetails))

    result = create_vpn(vpnDetails)
    if result.get("tf_return_code") == 0:
        return result, 201
    else:
        abort(500, "Failed to deploy your vpn ")


def delete(oid):
    logger.debug("Id is {}".format(oid))

    vpnDetails = {"id": oid}
    result = delete_vpn(vpnDetails)
    if result.get("tf_return_code") == 0:
        return {}, 200
    else:
        abort(500, "Failed to delete  your vpn ")


def create_async(vpnDetails):
    logger.debug(pformat(vpnDetails))

    result = create_vpn_task.delay(vpnDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def delete_async(oid):
    logger.debug("Id is {}".format(oid))

    vpnDetails = {"id": oid}

    result = delete_vpn_task.delay(vpnDetails=vpnDetails)

    logger.info("Task ID %s", result.task_id)

    context = {"taskid": result.task_id}

    return context, 201


def create_vpn_result(taskid):
    logger.info("CREATE VPN RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        logger.debug("retval %s", retval)
        tf_outputs: dict = retval["tf_outputs"]
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
            payload = {}
        else:
            payload = tf_outputs
            keys_to_remove = ['billing_account']
            remove_keys_from_dict(payload, keys_to_remove)
        return {'status': status, "payload": json.dumps(payload)}
    else:
        return {'status': status}


def delete_vpn_result(taskid):
    logger.info("DELETE VPN RESULT %s", format(taskid))
    status = AsyncResult(taskid).status
    if status == states.SUCCESS or status == states.FAILURE:
        retval = AsyncResult(taskid).get(timeout=1.0)
        return_code = retval["tf_return_code"]
        if return_code > 0:
            status = states.FAILURE
        return {'status': status}
    else:
        return {'status': status}
