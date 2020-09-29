# DESCRIPTION
# This test uploads the "UC Berkeley Home IP Web Trace" dataset in chunks of 100000 records. After each
# chunk a evaluation phase is triggered where randomly generated queries are submitted to the datastore.
# The goal of this testcase is to examin the response time behaviour of queries to the current state of the dataset
# in terms of dataset size.
import functools
import json
import os
import timeit

import numpy

import evaluation.util.ckan as ckan
from evaluation.tests import GenericNonFunctionalTest
from evaluation.util import mongodb

RESULT_FILE_HEADER = 'filter;fulltext\n'

RESULTS_DIR = os.environ.get('RESULTS_DIR')
CHUNK_SIZE = 10000


def do_loadtest(queries, iterations=1):
    response_times = []
    for query in queries:
        response_times += timeit.repeat(query, repeat=iterations, number=1)
    return numpy.average(response_times)


def fulltext_query(resource_id, query):
    ckan.datastore_search(resource_id=resource_id, q=query)


def filter_query(resource_id, statement):
    ckan.datastore_search(resource_id=resource_id, filter=statement)


class PerformanceQueryCurrentStateTest(GenericNonFunctionalTest):

    def __init__(self, results_dir, name, dataset, chunk_size, test_interval):
        super(PerformanceQueryCurrentStateTest, self).__init__(results_dir, name, dataset, chunk_size, test_interval)
        self._resource_id = None

    def _prepare_preconditions(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')

        ckan.ensure_package_does_not_exist('ucbtrace')
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
                                                primary_key='id')

        self.filter_queries = self._random_query_generator.generate_random_queries(size=20)
        self.fulltext_queries = ['GET', 'gif', 'html']

        with open(os.path.join(self.results_dir, 'csv', f'{self.tag}_nftc1_result.csv'), 'a') as result_file:
            result_file.writelines(RESULT_FILE_HEADER)

    def _do_evaluation(self):
        with open(os.path.join(self.results_dir, 'csv', f'{self.tag}_nftc1_result.csv'), 'a') as result_file:
            filter_queries = list(
                map(lambda query: functools.partial(filter_query, self._resource_id, query), self.filter_queries))
            filter_result = do_loadtest(filter_queries)

            fulltext_queries = list(
                map(lambda query: functools.partial(fulltext_query, self._resource_id, query),
                    self.fulltext_queries))
            fulltext_result = do_loadtest(fulltext_queries)

            result_file.writelines(f"{filter_result};{fulltext_result}\n")
