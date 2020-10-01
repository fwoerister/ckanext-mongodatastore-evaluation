import evaluation.util.ckan as ckan
import evaluation.util.hash as hash
from evaluation.tests import GenericFunctionalTest
from evaluation.tests.functional.static_test_assets import PACKAGE, RESOURCE_FILE_LOCATION


class QueryByValueFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(QueryByValueFunctionalTest, self).__init__(results_dir, name)
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
        self.logger.info("submit query...")
        self._query_result = ckan.client.action.datastore_search(resource_id=self._resource_id,
                                                                 filters={'Country': 'Austria'}, offset=0,
                                                                 limit=100)

    def _check_postcondition(self):
        ckan.verify_resultset_record_count(self._query_result, 64)
        hash.verify_hash(self._query_result, "3a7777e3a648d1fd1731ab1f25bae88d")
