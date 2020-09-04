# DESCRIPTION
# Delete records of an existing datastore resource.

import evaluation.util.ckan as ckan
import evaluation.util.env as env
import evaluation.util.mongodb as mongodb
from evaluation.tests import GenericFunctionalTest


class DeleteRecordFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(DeleteRecordFunctionalTest, self).__init__(results_dir, name)
        self._resource_id = None

    def _check_precondition(self):
        env.verify_containers_are_running()
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
        ckan.verify_package_does_exist('rr-experiment')
        self._resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})
        ckan.verify_record_with_id_exists(self._resource_id, 2)

    def _execute_steps(self):
        ckan.client.action.datastore_delete(resource_id=self._resource_id, filters={'id': 2}, force=True)

    def _check_postcondition(self):
        mongodb.verify_document_was_marked_as_deleted(self._resource_id, 2)
        ckan.verify_record_with_id_does_not_exist(self._resource_id, 2)