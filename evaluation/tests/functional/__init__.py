from evaluation.tests.functional.ftc1_1_publish_resource import PublishResourceFunctionalTest
from evaluation.tests.functional.ftc2_1_insert_record import InsertRecordFunctionalTest
from evaluation.tests.functional.ftc2_2_modify_record import ModifyRecordFunctionalTest
from evaluation.tests.functional.ftc2_3_delete_record import DeleteRecordFunctionalTest
from evaluation.tests.functional.ftc3_1_query_by_value import QueryByValueFunctionalTest
from evaluation.tests.functional.ftc3_2_range_query import RangeQueryFunctionalTest
from evaluation.tests.functional.ftc3_3_fulltext_query import FulltextQueryFunctionalTest
from evaluation.tests.functional.ftc3_4_sorted_query import SortedQueryFunctionalTest
from evaluation.tests.functional.ftc4_1_pid_for_query_by_value import PidForQueryByValueFunctionalTest
from evaluation.tests.functional.ftc4_2_pid_for_range_query import PidForRangeQueryFunctionalTest
from evaluation.tests.functional.ftc4_3_pid_for_fulltext_query import PidForFulltextQueryFunctionalTest
from evaluation.tests.functional.ftc4_4_pid_for_sorted_query import PidForSortedQueryFunctionalTest
from evaluation.tests.functional.ftc5_1_experiment_fetch_data_via_rest import ExperimentRestFunctionalTest
from evaluation.tests.functional.ftc5_2_experiment_fetch_data_via_cli import ExperimentCliFunctionalTest


def initialize(results_dir):
    return {
        '1.1': PublishResourceFunctionalTest(results_dir, 'ftc1_1_publish_resource'),
        '2.1': InsertRecordFunctionalTest(results_dir, 'ftc2_1_insert_record'),
        '2.2': ModifyRecordFunctionalTest(results_dir, 'ftc2_2_modify_record'),
        '2.3': DeleteRecordFunctionalTest(results_dir, 'ftc2_3_delete_record'),
        '3.1': QueryByValueFunctionalTest(results_dir, 'ftc3_1_query_by_value.py'),
        '3.2': RangeQueryFunctionalTest(results_dir, 'ftc3_2_range_query.py'),
        '3.3': FulltextQueryFunctionalTest(results_dir, 'ftc3_3_fulltext_query.py'),
        '3.4': SortedQueryFunctionalTest(results_dir, 'ftc3_4_sorted_query.py'),
        '4.1': PidForQueryByValueFunctionalTest(results_dir, 'ftc4_1_pid_for_query_by_value.py'),
        '4.2': PidForRangeQueryFunctionalTest(results_dir, 'ftc4_2_pid_for_range_query.py'),
        '4.3': PidForFulltextQueryFunctionalTest(results_dir, 'ftc4_3_pid_for_fulltext_query.py'),
        '4.4': PidForSortedQueryFunctionalTest(results_dir, 'ftc4_4_pid_for_sorted_query.py'),
        '5.1': ExperimentRestFunctionalTest(results_dir, 'ftc5_1_experiment_fetch_data_via_rest'),
        '5.2': ExperimentCliFunctionalTest(results_dir, 'ftc5_2_experiment_fetch_data_via_cli')
    }


