# DESCRIPTION
# In this testcase a query is submitted to the datastore that retrieves all
# records where a specific record field applies to a fulltext query.

import evaluation.util.ckan as ckan
import evaluation.util.env as env
import evaluation.util.hash as hash
from evaluation.tests import GenericFunctionalTest
from evaluation.tests.functional.static_test_assets import PACKAGE, RESOURCE_FILE_LOCATION


class FulltextQueryFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(FulltextQueryFunctionalTest, self).__init__(results_dir, name)
        self._resource_id = None
        self._query_result = None

    def _check_precondition(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
        ckan.reset_package_to_initial_state(PACKAGE, RESOURCE_FILE_LOCATION)

        ckan.verify_package_does_exist('rr-dataset')
        self._resource_id = ckan.verify_package_contains_resource('rr-dataset',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})

    def _execute_steps(self):
        self._query_result = ckan.client.action.datastore_search(resource_id=self._resource_id, q="Aus", offset=0,
                                                                 limit=200)

    def _check_postcondition(self):
        ckan.verify_resultset_record_count(self._query_result, 130)
        hash.verify_hash(self._query_result, "9d5a7a39934843f9fa147d929a63279e")
