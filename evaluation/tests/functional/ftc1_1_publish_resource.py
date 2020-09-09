# DESCRIPTION
# The objective of this tests case is to evaluate the publication feature
# of the proposed system by uploading the datasets of the Reinhard & Rogoff
# experiment to it. This will also cover the publication of the related metadata
# of the published datasets.

from time import sleep

import evaluation.util.ckan as ckan
import evaluation.util.env as env
import evaluation.util.solr as solr
from evaluation.tests import GenericFunctionalTest


class PublishResourceFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(PublishResourceFunctionalTest, self).__init__(results_dir, name)
        self._resource = None

    def _check_precondition(self):
        #env.verify_containers_are_running()
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
        ckan.ensure_package_does_not_exist('rr-experiment')

    def _execute_steps(self):
        self.logger.debug("execute test steps...")
        package = ckan.client.action.package_create(name='rr-experiment', title='Reinhard&Rogoff Experiment Data',
                                                    private=False,
                                                    owner_org='dc13c7c9-c3c9-42ac-8200-8fe007c049a1',
                                                    author='Carmen Reinhart; Kenneth Rogoff',
                                                    maintainer='', license='other-open',
                                                    extras=[{'key': 'year', 'value': '2010'}])

        self._resource = ckan.client.action.resource_create(package_id=package['id'],
                                                            name='countries_dataset.csv',
                                                            upload=open('data/datasets/countries_dataset.csv', 'r'))

        self.logger.info("wait 10 seconds for datapusher...")
        sleep(10)

    def _check_postcondition(self):
        # *) package was indexed
        solr.index_exists('rr-experiment')

        # *) the package is stored in ckan
        package = ckan.client.action.package_show(id='rr-experiment')
        assert (package is not None)

        # *) the metadata is stored in ckan
        assert (package['author'] == 'Carmen Reinhart; Kenneth Rogoff')
        assert (package['extras'] == [{'key': 'year', 'value': '2010'}])
