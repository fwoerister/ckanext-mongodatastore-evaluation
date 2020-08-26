# DESCRIPTION
#
import json
import os
import timeit

import numpy

import evaluation.util.ckan as ckan
from evaluation.tests import GenericNonFunctionalTest


class PerformanceIndexUsage(GenericNonFunctionalTest):

    def __init__(self, results_dir, name, dataset, chunksize):
        super(PerformanceIndexUsage, self).__init__(results_dir, name, dataset, chunksize)
        self._queries = None

    def _prepare_preconditions(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
        package_id = ckan.verify_package_does_exist('rr-experiment')

        self._resource_id = ckan.client.action.resource_create(package_id=package_id,
                                                               name='UC Berkeley Home IP Web Trace')['id']

        with open('data/datasets/trace_fields.json', 'r') as trace_fields:
            ckan.client.action.datastore_create(resource_id=self._resource_id, force='True',
                                                fields=json.load(trace_fields),
                                                primary_key='id')

        self._resource_id_idx = ckan.client.action.resource_create(package_id=package_id,
                                                                   name='UC Berkeley Home IP Web Trace - Idx')['id']

        with open('data/datasets/trace_fields.json', 'r') as trace_fields:
            ckan.client.action.datastore_create(resource_id=self._resource_id_idx, force='True',
                                                fields=json.load(trace_fields),
                                                indexes="client_port",
                                                primary_key='id')

        self._queries = self._random_query_generator.generate_random_queries(10, ['client_port'])

    def _do_evaluation(self):
        response_time = []
        response_time_idx = []
        for query in self._queries:
            response_time = timeit.repeat(lambda: ckan.client.action.datastore_search(resource_id=self._resource_id,
                                                                                      statement=query,
                                                                                      limit=100), repeat=10, number=1)
            response_time_idx = timeit.repeat(
                lambda: ckan.client.action.datastore_search(resource_id=self._resource_id_idx,
                                                            statement=query,
                                                            limit=100), repeat=10, number=1)

        with open(os.path.join(self.results_dir, 'csv', 'nftc3_response_times.csv'), 'a') as result_file:
            result_file.writelines(f'{numpy.average(response_time)}\n')

        with open(os.path.join(self.results_dir, 'csv', 'nftc3_response_times_idx.csv'), 'a') as result_file:
            result_file.writelines(f'{numpy.average(response_time_idx)}\n')
