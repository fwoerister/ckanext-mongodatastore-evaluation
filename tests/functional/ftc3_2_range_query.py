import logging

import evalutil.ckan as ckan
import evalutil.env as env

# DESCRIPTION
# In this testcase a query is submitted to the datastore that
# retrieves all records where a specific record field applies
# to a range of values. For the resulting datasets a PID is issued.
import evalutil.hash

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logging.info("Start execution of 'tc3_2'")

# PRE-REQUISIT
env.verify_containers_are_running()
ckan.verify_if_evaluser_exists()
ckan.verify_if_organization_exists('tu-wien')
ckan.verify_package_does_exist('rr-experiment')
resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                    {'name': 'countries_dataset.csv', 'datastore_active': True})

logging.info("pre-requisists are fullfilled")

# STEPS
result = ckan.client.action.datastore_search(resource_id=resource_id, filters={'Debt': '>200000000'}, offset=0, limit=100)

# EXPECTED RESULTS
ckan.verify_resultset_record_count(result, 22)
evalutil.hash.verify_hash(result, "2ed7dfa1f144a1023992d407c359fad9")

logging.info("'tc3_2' successfully executed!")
