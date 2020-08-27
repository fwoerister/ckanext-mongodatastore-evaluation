# DESCRIPTION
import evaluation.util.ckan as ckan
from evaluation.tests import GenericNonFunctionalTest


class PerformanceShardingTest(GenericNonFunctionalTest):
    def __init__(self, results_dir, name, dataset, chunksize, test_interval):
        super(PerformanceShardingTest, self).__init__(results_dir, name, dataset, chunksize, test_interval)

    def _prepare_preconditions(self):
        ckan.verify_if_evaluser_exists()
        ckan.verify_if_organization_exists('tu-wien')
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

    def _do_evaluation(self):
        super()._do_evaluation()

    def _after_upload(self):
        # todo: do evaluation
        pass
