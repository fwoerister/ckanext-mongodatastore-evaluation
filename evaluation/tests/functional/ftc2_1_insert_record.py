# DESCRIPTION
# Insert new records to an existing datastore resource.

import evaluation.util.ckan as ckan
import evaluation.util.env as env
import evaluation.util.mongodb as mongodb
from evaluation.tests import GenericFunctionalTest

NEW_RECORD = {'id': 1276, 'Country': 'Australia', 'Year': 2010, 'Debt': 101136.25205, 'RGDP': None, 'GDP': None,
              'dRGDP': 0.732249739168633, 'GDPI': 109.15168, 'GDP1': None, 'GDP2': 1201390, 'RGDP1': None,
              'RGDP2': 1100661, 'GDPI1': None, 'GDPI2': None, 'Infl': '1.629', 'Debt1': None, 'Debt2': None,
              'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': 8.41826984160015,
              'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': 1092660}


class InsertRecordFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(InsertRecordFunctionalTest, self).__init__(results_dir, name)
        self._resource_id = None

    def _check_precondition(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')

        ckan.verify_package_does_exist('rr-experiment')
        self._resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})

        mongodb.remove_datastore_entries_by_id(self._resource_id, 1276)

    def _execute_steps(self):
        ckan.client.action.datastore_upsert(resource_id=self._resource_id, force=True, records=[NEW_RECORD],
                                            method='insert')

    def _check_postcondition(self):
        mongodb.verify_new_document_is_in_mongo_collection(self._resource_id, NEW_RECORD)
        ckan.verify_new_record_is_in_datastore(self._resource_id, NEW_RECORD)
