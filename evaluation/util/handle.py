import json
import logging

from easyhandle.client import BasicAuthHandleClient

STREAM_TEMPLATE = '{}/storedquery/{}/dump'
API_TEMPLATE = '{}/api/3/action/querystore_resolve?id={}'
URL_TEMPLATE = '{}/storedquery/landingpage?id={}'

logger = logging.getLogger(__name__)

config = json.load(open('config.json', 'r'))
client = BasicAuthHandleClient.load_from_config(config['handle'])


def verify_handle_resolves_to_pid(handle_pid, internal_id):
    result = client.get_handle(handle_pid)
    values = result.json()['values']

    for value in values:
        if value['type'] == 'URL':
            assert value['data']['value'] == URL_TEMPLATE.format(config['ckan']['site_url'], internal_id)
        elif value['type'] == 'API_URL':
            assert value['data']['value'] == API_TEMPLATE.format(config['ckan']['site_url'], internal_id)
        elif value['type'] == 'STREAM_URL':
            assert value['data']['value'] == STREAM_TEMPLATE.format(config['ckan']['site_url'], internal_id)
