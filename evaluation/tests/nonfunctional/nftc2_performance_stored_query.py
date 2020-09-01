# DESCRIPTION
# This test uploads the forst 1 000 000 records of the "UC Berkeley Home IP Web Trace" dataset to a ckan datastore.
# On the first million records 10 PIDs are issued (random queries). Then the remaining records are pushed to
# datastore in chunks of 10 000 records. After each chunk the time for retrieving the persistently identified
# data subsets is measured
import json
import os
import timeit

import numpy

import evaluation.util.ckan as ckan
import evaluation.util.mongodb as mongodb
from evaluation.tests import GenericNonFunctionalTest
from evaluation.util.trace import line_to_trace_record


class PerformanceStoredQueryTest(GenericNonFunctionalTest):

    def __init__(self, results_dir, name, dataset, chunksize, test_interval):
        super().__init__(results_dir, name, dataset, chunksize, test_interval)
        self._pids = []
        self._resource_id = None

    def _prepare_preconditions(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')

        mongodb.purge_indexes('CKAN_Datastore')

        ckan.ensure_package_does_not_exist('ucbtrace')
        package = ckan.client.action.package_create(name='ucbtrace', title='UC Berkeley Home IP Web Traces',
                                                    private=False,
                                                    owner_org='dc13c7c9-c3c9-42ac-8200-8fe007c049a1',
                                                    author='Steve Gribble',
                                                    maintainer='', license='other-open',
                                                    extras=[{'key': 'year', 'value': '2017'}])

        self._resource_id = ckan.client.action.resource_create(package_id=package['id'],
                                                               name='UC Berkeley Home IP Web Trace')['id']

        with open('data/datasets/trace_fields.json', 'r') as trace_fields:
            ckan.client.action.datastore_create(resource_id=self._resource_id, force='True',
                                                fields=json.load(trace_fields),
                                                primary_key='id')

        with(open('data/datasets/preprocessed_trace_1000000')) as trace_file:
            line_count = 1
            records = []
            while line := trace_file.readline():
                records.append(line_to_trace_record(line, line_count))

                if line_count % self._chunksize == 0:
                    self.logger.info(f'{str(line_count).rjust(8," ")} records uploaded')
                    ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=records,
                                                        force=True, method='insert')
                    records = []

                line_count += 1

        filter_queries = self._random_query_generator.generate_random_queries(size=10)
        fulltext_queries = ['GET', 'gif', 'html']

        for query in filter_queries:
            self._pids.append(ckan.client.action.issue_pid(resource_id=self._resource_id,
                                                           statement=query))

        for query in fulltext_queries:
            self._pids.append(ckan.client.action.issue_pid(resource_id=self._resource_id,
                                                           q=query))

    def _do_evaluation(self):
        results = []

        for pid in self._pids:
            results.append(timeit.repeat(lambda: ckan.client.action.querystore_resolve(pid=pid, limit=100),
                                         repeat=5,
                                         number=1))

        with open(os.path.join(self.results_dir, 'csv', f'{self.tag}_nftc2_response_times.csv'), 'a') as result_file:
            result_file.writelines(f'{numpy.average(results)}\n')
