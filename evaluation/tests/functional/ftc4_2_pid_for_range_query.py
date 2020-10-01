# DESCRIPTION
# In this testcase a query is submitted to the datastore that retrieves all records where a specific
# field matches a range query. For the resulting datasets a PID is issued.

from time import sleep

import evaluation.util.ckan as ckan
import evaluation.util.env as env
import evaluation.util.handle as handle
import evaluation.util.hash as hash
import evaluation.util.querystore as querystore
from evaluation.tests import GenericFunctionalTest
from evaluation.tests.functional.static_test_assets import PACKAGE, RESOURCE_FILE_LOCATION


class PidForRangeQueryFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(PidForRangeQueryFunctionalTest, self).__init__(results_dir, name)
        self._resource_id = None
        self._pid = None
        self._stored_query_results = []

    def _check_precondition(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
        ckan.reset_package_to_initial_state(PACKAGE, RESOURCE_FILE_LOCATION)

        ckan.verify_package_does_exist('rr-dataset')
        self._resource_id = ckan.verify_package_contains_resource('rr-dataset',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})

    def _execute_steps(self):
        self._pid = ckan.client.action.issue_pid(resource_id=self._resource_id, statement={'Debt': '>200000000'},
                                                 sort='Infl asc')

        sleep(5)
        self.logger.info("wait 5 seconds for background job to finish...")

        self._stored_query_results.append(ckan.client.action.querystore_resolve(id=self._pid))

        new_record = {'id': 1278, 'Country': 'Australia', 'Year': 2010, 'Debt': 101136.25205, 'RGDP': None, 'GDP': None,
                      'dRGDP': 0.732249739168633, 'GDPI': 109.15168, 'GDP1': None, 'GDP2': 1201390, 'RGDP1': None,
                      'RGDP2': 1100661, 'GDPI1': None, 'GDPI2': None, 'Infl': '1.629', 'Debt1': None, 'Debt2': None,
                      'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': 8.41826984160015,
                      'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': 1092660}
        ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=[new_record], method='insert',
                                            force=True)
        self._stored_query_results.append(ckan.client.action.querystore_resolve(id=self._pid))

        new_record = {'id': 1, 'Country': 'Australia', 'Year': 2000, 'Debt': None, 'RGDP': None, 'GDP': None,
                      'dRGDP': None, 'GDPI': None, 'GDP1': None, 'GDP2': None, 'RGDP1': None,
                      'RGDP2': None, 'GDPI1': None, 'GDPI2': None, 'Infl': None, 'Debt1': None, 'Debt2': None,
                      'Debtalt': 1234, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': None,
                      'GDP3': None, 'GNI': None, 'lRGDP': 1234, 'lRGDP1': None, 'lRGDP2': None}

        ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=[new_record], method='upsert',
                                            force=True)
        self._stored_query_results.append(ckan.client.action.querystore_resolve(id=self._pid))

        ckan.client.action.datastore_delete(resource_id=self._resource_id, filters={'Country': 'Japan'}, force=True)
        self._stored_query_results.append(ckan.client.action.querystore_resolve(id=self._pid))

    def _check_postcondition(self):
        hash.verify_all_elements_have_same_hash(self._stored_query_results, hash.calculate_hash)
        handle_pid = querystore.verify_handle_was_assigned(self._pid)
        handle.verify_handle_resolves_to_pid(handle_pid, self._pid)
