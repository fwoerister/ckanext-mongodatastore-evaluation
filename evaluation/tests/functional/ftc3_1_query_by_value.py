# DESCRIPTION
# In this testcase a query is submitted to the datastore that retrieves all records where a specific
# field exactly matches the provided parameter. For the resulting datasets a PID is issued.

import evaluation.util.ckan as ckan
import evaluation.util.env as env
import evaluation.util.hash as hash
from evaluation.tests import GenericFunctionalTest


class QueryByValueFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(QueryByValueFunctionalTest, self).__init__(results_dir, name)
        self._resource_id = None
        self._query_result = None

    def _check_precondition(self):
        #env.verify_containers_are_running()
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
        ckan.verify_package_does_exist('rr-experiment')
        self._resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})

    def _execute_steps(self):
        self._query_result = ckan.client.action.datastore_search(resource_id=self._resource_id,
                                                                 filters={'Country': 'Austria'}, offset=0,
                                                                 limit=100)

    def _check_postcondition(self):
        ckan.verify_resultset_record_count(self._query_result, 64)
        hash.verify_hash(self._query_result, "3a7777e3a648d1fd1731ab1f25bae88d")
