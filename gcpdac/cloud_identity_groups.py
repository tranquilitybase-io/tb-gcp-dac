from typing import Any, Union

from flask import Response
from googleapiclient.discovery import Resource

import config
import requests

from google.oauth2 import service_account
import googleapiclient.discovery

SCOPES = ['https://www.googleapis.com/auth/cloud-identity.groups']
# SERVICE_ACCOUNT_FILE = '/path/to/service-account-file.json'
SERVICE_ACCOUNT_FILE = '/credentials.json'
SERVICE_ACCOUNT = 'bootstrap-sa@bootstrap-xe68ff2g.iam.gserviceaccount.com'

logger = config.logger


# https://cloud.google.com/identity/docs/how-to/setup
# https://developers.google.com/identity/protocols/oauth2/web-server#python_1
# https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred

def read_all():
    logger.debug("read_all")
    service = create_service()
    logger.debug("service created")

    identity_source_id = "C02tnxhq5"
    data = search_identity_groups(service, identity_source_id, "10", "View.BASIC")
    data = list_identity_groups(service, identity_source_id, "10", "View.BASIC")
    # service.groups().
    # r: Response = requests.get("https://cloudidentity.googleapis.com/v1/groups")
    # logger.debug("response is {} ".format(r))
    # data = r.json()
    # logger.debug("response data is {} ".format(data))
    # groups = data["groups"]
    # for group in groups:
    #     logger.debug("group is {} ".format(group))
    #
    return data


def search_identity_groups(service, identity_source_id, pageSize, view):
    # Set the label to search for all identity groups
    searchQuery = "&query=namespace=identitysources/" + identity_source_id \
                  + "%20AND%20" + "labels:system/groups/external"
    # + "&pageSize=" + pageSize\
    # + "&view=" + view
    try:
        searchGroupsRequest = service.groups().search()
        searchGroupsRequest.uri += searchQuery
        response = searchGroupsRequest.execute()
        logger.debug("response: {}".format(response))
    except Exception as e:
        logger.debug(e)


def list_identity_groups(service, identity_source_id, pageSize, view):
    # Set the label to search for all identity groups
    listQuery = "&parent=identitysources/" + identity_source_id
    # + "%20AND%20" + "&pageSize=" + pageSize
    # + "&view=" + view
    try:
        listGroupsRequest = service.groups().list()
        listGroupsRequest.uri += listQuery
        response = listGroupsRequest.execute()
        logger.debug("response: {}".format(response))
    except Exception as e:
        logger.debug(e)


def create_service():
    logger.debug("create_service")
    service: Resource = None
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        logger.debug("credentials {}".format(credentials))

        service_name = 'cloudidentity.googleapis.com'
        api_version = 'v1'
        discovery_url = (
                'https://%s/$discovery/rest?version=%s' % (service_name, api_version))
        service: Resource = googleapiclient.discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=credentials)
        logger.debug("service {}".format(service))
    except Exception as e:
        logger.debug("exception {}".format(e))

    return service
