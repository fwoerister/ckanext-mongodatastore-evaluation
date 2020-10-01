import evaluation.util.ckan as ckan
import evaluation.util.mongodb as mongodb
from evaluation.tests import GenericFunctionalTest
from evaluation.tests.functional.static_test_assets import PACKAGE, RESOURCE_FILE_LOCATION, NEW_RECORD


class InsertRecordFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(InsertRecordFunctionalTest, self).__init__(results_dir, name)
        self._resource_id = None

    def _check_precondition(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')

        ckan.reset_package_to_initial_state(PACKAGE, RESOURCE_FILE_LOCATION)

        ckan.verify_package_does_exist('rr-dataset')
        self._resource_id = ckan.verify_package_contains_resource('rr-dataset',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})

    def _execute_steps(self):
        self.logger.info("insert record...")
        ckan.client.action.datastore_upsert(resource_id=self._resource_id, force=True, records=[NEW_RECORD],
                                            method='insert')

    def _check_postcondition(self):
        mongodb.verify_new_document_is_in_mongo_collection(self._resource_id, NEW_RECORD)
        ckan.verify_new_record_is_in_datastore(self._resource_id, NEW_RECORD)
