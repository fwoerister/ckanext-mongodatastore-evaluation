# DESCRIPTION
from evaluation.tests import GenericNonFunctionalTest


class PerformanceShardingTest(GenericNonFunctionalTest):
    def __init__(self, results_dir, name, dataset, chunksize, test_interval):
        super(PerformanceShardingTest, self).__init__(results_dir, name, dataset, chunksize, test_interval)

    def _prepare_preconditions(self):
        pass

    def _do_evaluation(self):
        pass