# DESCRIPTION
#

import functools
import os
import timeit

import numpy

import evaluation.util.ckan as ckan
from evaluation.tests.nonfunctional import PerformanceQueryCurrentStateTest

RESULTS_DIR = os.environ.get('RESULTS_DIR')
CHUNK_SIZE = 10000


def do_loadtest(queries, iterations=1):
    response_times = []
    for query in queries:
        response_times += timeit.repeat(query, repeat=iterations, number=1)
    return numpy.average(response_times)


def nv_fulltext_query(resource_id, query):
    ckan.nv_datastore_search(resource_id=resource_id, q=query)


def nv_filter_query(resource_id, statement):
    ckan.nv_datastore_search(resource_id=resource_id, filter=statement)


class PerformanceNonVersionedMongoResource(PerformanceQueryCurrentStateTest):

    def __init__(self, results_dir, name, dataset, chunk_size, test_interval):
        super(PerformanceNonVersionedMongoResource, self).__init__(results_dir, name, dataset, chunk_size,
                                                                   test_interval)

    def _do_evaluation(self):
        with open(os.path.join(self.results_dir, 'csv', f'{self.tag}_nftc2_result.csv'), 'a') as result_file:
            nv_filter_queries = list(
                map(lambda query: functools.partial(nv_filter_query, self._resource_id, query), self.filter_queries))
            nv_filter_result = do_loadtest(nv_filter_queries)

            nv_fulltext_queries = list(
                map(lambda query: functools.partial(nv_fulltext_query, self._resource_id, query),
                    self.fulltext_queries))
            nv_fulltext_result = do_loadtest(nv_fulltext_queries)

            result_file.writelines(f"{nv_filter_result};{nv_fulltext_result}\n")
