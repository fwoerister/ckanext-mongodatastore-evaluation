# DESCRIPTION
# Update exsting records of an datastore resource.

import evaluation.util.ckan as ckan
import evaluation.util.env as env
import evaluation.util.mongodb as mongodb
from evaluation.tests import GenericFunctionalTest
from evaluation.tests.functional.static_test_assets import PACKAGE, RESOURCE_FILE_LOCATION, MODIFIED_RECORD


class ModifyRecordFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(ModifyRecordFunctionalTest, self).__init__(results_dir, name)
        self._resource_id = None

    def _check_precondition(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')

        ckan.reset_package_to_initial_state(PACKAGE, RESOURCE_FILE_LOCATION)

        ckan.verify_package_does_exist('rr-experiment')
        self._resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})
        ckan.verify_record_with_id_exists(self._resource_id, 1)

    def _execute_steps(self):
        ckan.client.action.datastore_upsert(resource_id=self._resource_id, force=True, records=[MODIFIED_RECORD],
                                            method='upsert')

    def _check_postcondition(self):
        internal_record = mongodb.db.get_collection(self._resource_id).find_one(MODIFIED_RECORD)
        assert (internal_record is not None)

        # A timestamp was added to the record that represents the point of time when the record was added to the resource
        assert (internal_record['_created'] is not None)

        # A timestamp '_valid_to' was attached to the older version of the record
        old_record = mongodb.db.get_collection(self._resource_id).find_one({'id': 1, '_latest': False})
        assert (old_record['_valid_to'] is not None)
