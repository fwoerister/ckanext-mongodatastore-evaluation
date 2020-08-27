from evaluation.tests.nonfunctional.nftc1_performance_query_current_state import PerformanceQueryCurrentStateTest
from evaluation.tests.nonfunctional.nftc2_performance_stored_query import PerformanceStoredQueryTest
from evaluation.tests.nonfunctional.nftc3_performance_with_index import PerformanceIndexUsage

TRACE_DATASET = 'data/datasets/preprocessed_trace'
TRACE_REMAINING = 'data/datasets/preprocessed_trace_remaining'


def initialize(results_dir):
    return {
        '1': PerformanceQueryCurrentStateTest(results_dir, 'nftc1_performance_query_current_state',
                                              TRACE_DATASET, 10000, 500000),
        '2': PerformanceStoredQueryTest(results_dir, 'nftc2_performance_stored_query',
                                        TRACE_REMAINING, 10000, 500000),
        '3': PerformanceIndexUsage(results_dir, 'nftc3_performance_with_index',
                                   TRACE_DATASET, 10000, 500000),
    }
