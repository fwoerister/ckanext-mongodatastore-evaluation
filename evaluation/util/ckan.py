import json
import logging
import os
from time import sleep

import ckanapi
import requests
from ckanapi import NotFound

logger = logging.getLogger(__name__)

config = json.load(open('config.json', 'r'))
client = ckanapi.RemoteCKAN(config['ckan']['base_url'], apikey=config['ckan']['apikey'])

HOST = 'http://ckan:5000'


def verify_if_evaluser_exists():
    username = config['ckan']['evaluser']
    result = client.action.user_show(id=username)
    assert (result is not None)


def verify_if_organization_exists(org_name):
    result = client.action.organization_show(id=org_name)
    assert (result is not None)


def ensure_package_does_not_exist(pkg_name):
    try:
        client.action.package_delete(id=pkg_name)
    except NotFound:
        logger.info("tried to delete non-existing package")


def verify_package_does_exist(pkg_name):
    try:
        pkg = client.action.package_show(id=pkg_name)
        return pkg['id']
    except NotFound as e:
        raise AssertionError(e)


def reset_package_to_initial_state(package, resource_file):
    ensure_package_does_not_exist(package['name'])

    package = client.action.package_create(**package)

    resource = client.action.resource_create(package_id=package['id'],
                                             name=os.path.basename(resource_file), upload=open(resource_file, 'r'))

    sleep(10)

    return resource['id']


def verify_package_contains_resource(pkg_name, expected_resource):
    package = client.action.package_show(id=pkg_name)

    assert (len(package['resources']) == 1)
    resource = package['resources'][0]

    assert (resource['name'] == expected_resource['name'])
    assert (resource['datastore_active'] == expected_resource['datastore_active'])
    return resource['id']


def verify_new_record_is_in_datastore(resource_id, new_record):
    result = client.action.datastore_search(resource_id=resource_id, filters={'id': new_record['id']})
    assert (len(result['records']) == 1)
    assert (result['records'][0] == new_record)


def verify_record_with_id_exists(resource_id, record_id):
    result = client.action.datastore_search(resource_id=resource_id, filters={'id': record_id})
    assert (len(result['records']) == 1)


def verify_record_with_id_does_not_exist(resource_id, record_id):
    result = client.action.datastore_search(resource_id=resource_id, filters={'id': record_id})
    assert (len(result['records']) == 0)


def verify_resultset_record_count(result, expected_count):
    assert result['total'] == len(result['records']), \
        "number of returned records and 'total' field do not match ({} vs {})".format(result['total'],
                                                                                      len(result['records']))

    assert result['total'] == expected_count, f"expected {expected_count} records but retrieved {result['total']}"


def nv_datastore_search(resource_id, filter=None, q=None):
    url = f'{HOST}/api/3/action/nv_query?limit=500&resource_id={resource_id}'

    if filter:
        url += f'&filters={json.dumps(filter)}'
    if q:
        url += f'&q={q}'

    return requests.get(url).json()


def datastore_search(resource_id, filter=None, q=None):
    url = f'{HOST}/api/3/action/datastore_search?limit=500&resource_id={resource_id}'

    if filter:
        url += f'&filters={json.dumps(filter)}'
    if q:
        url += f'&q={q}'

    return requests.get(url).json()
