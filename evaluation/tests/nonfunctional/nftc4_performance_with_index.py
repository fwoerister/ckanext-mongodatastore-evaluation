# DESCRIPTION
#
import json
import os
import timeit
from time import sleep

import numpy

import evaluation.util.ckan as ckan
import evaluation.util.mongodb as mongodb
import evaluation.util.postgresql as postgresql
from evaluation.tests import GenericNonFunctionalTest

RESULT_FILE_HEADER = 'index;no index\n'


class PerformanceIndexUsage(GenericNonFunctionalTest):

    def __init__(self, results_dir, name, dataset, chunksize, test_interval, db_type='mongodb'):
        super(PerformanceIndexUsage, self).__init__(results_dir, name, dataset, chunksize, test_interval)
        self._queries = None
        self._db_type = db_type

    def _prepare_preconditions(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')

        ckan.ensure_package_does_not_exist('ucbtrace')
        if self._db_type == 'mongodb':
            mongodb.purge_indexes('CKAN_Datastore')

        package = ckan.client.action.package_create(name='ucbtrace', title='UC Berkeley Home IP Web Traces',
                                                    private=False,
                                                    owner_org='tu-wien',
                                                    author='Steve Gribble',
                                                    maintainer='', license='other-open',
                                                    extras=[{'key': 'year', 'value': '2017'}])

        self._resource_id = ckan.client.action.resource_create(package_id=package['id'],
                                                               name='UC Berkeley Home IP Web Trace')['id']

        with open('data/datasets/trace_fields.json', 'r') as trace_fields:
            ckan.client.action.datastore_create(resource_id=self._resource_id, force='True',
                                                fields=json.load(trace_fields),
                                                indexes="client_port",
                                                primary_key='id')

        self._queries = self._random_query_generator.generate_random_queries(20, ['client_port'])

    def _do_evaluation(self):
        super(PerformanceIndexUsage, self)._do_evaluation()

    def _after_upload(self):
        response_time = []
        response_time_idx = []
        for query in self._queries:
            response_time_idx.append(timeit.repeat(lambda: ckan.datastore_search(self._resource_id, filter=query),
                                                   repeat=1,
                                                   number=1))

        if self._db_type == 'mongodb':
            mongodb.purge_index(self._resource_id, 'client_port_index')
        else:
            postgresql.remove_index(self._resource_id, 'client_port')
        sleep(5)

        for query in self._queries:
            response_time.append(timeit.repeat(lambda: ckan.datastore_search(self._resource_id, filter=query),
                                               repeat=1,
                                               number=1))

        with open(os.path.join(self.results_dir, 'csv', f'{self.tag}_nftc4_response_times.csv'), 'a') as result_file:
            result_file.writelines(RESULT_FILE_HEADER)
            result_file.writelines(f'{numpy.average(response_time_idx)};{numpy.average(response_time)}\n')
