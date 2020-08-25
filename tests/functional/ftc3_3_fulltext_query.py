import logging

import evalutil.ckan as ckan
import evalutil.env as env

# DESCRIPTION
# In this testcase a query is submitted to the datastore that retrieves all
# records where a specific record field applies to a fulltext query.
import evalutil.hash

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logging.info("Start execution of 'tc3_3'")

# PRE-REQUISIT
env.verify_containers_are_running()
ckan.verify_if_evaluser_exists()
ckan.verify_if_organization_exists('tu-wien')
ckan.verify_package_does_exist('rr-experiment')
resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                    {'name': 'countries_dataset.csv', 'datastore_active': True})

logging.info("pre-requisists are fullfilled")

# STEPS
result = ckan.client.action.datastore_search(resource_id=resource_id, q="Aus", offset=0, limit=200)

# EXPECTED RESULTS
ckan.verify_resultset_record_count(result, 130)
evalutil.hash.verify_hash(result, "067e98c4b438b9de6dea49e63812f251")

logging.info("'tc3_3' successfully executed!")
