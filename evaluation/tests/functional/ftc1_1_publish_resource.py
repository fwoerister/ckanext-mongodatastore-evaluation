# DESCRIPTION
# The objective of this tests case is to evaluate the publication feature
# of the proposed system by uploading the datasets of the Reinhard & Rogoff
# experiment to it. This will also cover the publication of the related metadata
# of the published datasets.

from time import sleep

import requests

import evaluation.util.ckan as ckan
import evaluation.util.solr as solr
from evaluation.tests import GenericFunctionalTest


class PublishResourceFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(PublishResourceFunctionalTest, self).__init__(results_dir, name)
        self._resource = None

    def _check_precondition(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
        ckan.ensure_package_does_not_exist('rr-dataset')

    def _execute_steps(self):
        self.logger.debug("execute test steps...")
        package = ckan.client.action.package_create(name='rr-dataset', title='Reinhard&Rogoff Datasets',
                                                    private=False,
                                                    owner_org='tu-wien',
                                                    author='Carmen Reinhart; Kenneth Rogoff',
                                                    maintainer='', license='other-open',
                                                    extras=[{'key': 'year', 'value': '2010'}])

        self._resource = ckan.client.action.resource_create(package_id=package['id'],
                                                            name='countries_dataset.csv',
                                                            upload=open('data/datasets/countries_dataset.csv', 'r'))

        self.logger.info("wait 5 seconds for datapusher...")
        sleep(5)

    def _check_postcondition(self):
        # *) package was indexed
        solr.index_exists('rr-dataset')

        # *) the package is stored in ckan
        package = ckan.client.action.package_show(id='rr-dataset')
        assert (package is not None)

        # *) the metadata is stored in ckan
        assert (package['author'] == 'Carmen Reinhart; Kenneth Rogoff')
        assert (package['extras'] == [{'key': 'year', 'value': '2010'}])

        ckan.verify_package_contains_resource('rr-dataset',
                                              {'name': 'countries_dataset.csv',
                                               'datastore_active': True})
