from evaluation.tests.nonfunctional.nftc1_performance_query_current_state import PerformanceQueryCurrentStateTest
from evaluation.tests.nonfunctional.nftc2_performance_stored_query import PerformanceStoredQueryTest

TRACE_DATASET = 'data/datasets/preprocessed_trace'
TRACE_REMAINING = 'data/datasets/preprocessed_trace_remaining'


def initialize(results_dir):
    return {
        '1': PerformanceQueryCurrentStateTest(results_dir, 'nftc1_query_current_state', TRACE_DATASET, 10000),
        '2': PerformanceStoredQueryTest(results_dir, 'nftc2_stored_query', TRACE_REMAINING, 10000),
    }
