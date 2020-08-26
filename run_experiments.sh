#!/bin/bash
set -e
export PYTHONPATH=$PYTHONPATH:.

NOW=$(date +%s)
export RESULTS_DIR=results/"$NOW"_"$1"

rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR/csv"
mkdir -p "$RESULTS_DIR/log"
mkdir -p "$RESULTS_DIR/pdf"

# testing functional requirements
#python3 evaluation/tests/functional/ftc1_1_publish_resource.py
#python3 evaluation/tests/functional/ftc2_1_insert_record.py
#python3 evaluation/tests/functional/ftc2_2_modify_record.py
#python3 evaluation/tests/functional/ftc2_3_delete_record.py
#python3 evaluation/tests/functional/ftc3_1_query_by_value.py
#python3 evaluation/tests/functional/ftc3_2_range_query.py
#python3 evaluation/tests/functional/ftc3_3_fulltext_query.py
#python3 evaluation/tests/functional/ftc3_4_sorted_query.py
#python3 evaluation/tests/functional/ftc4_1_pid_for_query_by_value.py
#python3 evaluation/tests/functional/ftc4_2_pid_for_range_query.py
#python3 evaluation/tests/functional/ftc4_3_pid_for_fulltext_query.py
#python3 evaluation/tests/functional/ftc4_4_pid_for_sorted_query.py
#python3 evaluation/tests/functional/ftc5_1_experiment_fetch_data_via_rest.py
#python3 evaluation/tests/functional/ftc5_2_experiment_fetch_data_via_cli.py

# testing non-functional requirements
python3 evaluation/tests/nonfunctional/nftc1.py
python3 evaluation/tests/nonfunctional/nftc2.py
python3 evaluation/tests/nonfunctional/nftc3.py
python3 evaluation/tests/nonfunctional/nftc4.py

exit 0