import argparse
import os
import random
from datetime import datetime

import evaluation.tests.functional as f_tests
import evaluation.tests.nonfunctional as nf_tests

random.seed(4491)

parser = argparse.ArgumentParser(description='Run the evaluation experiments of the ckanext-mongodatastore project')
parser.add_argument('tag', type=str,
                    help='A tag that is included in the name of the results folder')
parser.add_argument('--functional', type=str, nargs='*', help=f'Available tests: ')
parser.add_argument('--nonfunctional', type=str, nargs='*')
args = parser.parse_args()


def check_testcase_labels(labels: list, tests: dict, testtype: str):
    if not labels:
        return True
    for label in labels:
        if label not in tests.keys():
            print(f"The provided testcase label {label} is not a valid {testtype} testcase.\n")
            print("Available testcases:")
            for key in tests.keys():
                print(f"\t*) {key}")
            return False
    return True


def main():
    now = int(datetime.now().timestamp())
    os.mkdir(results_dir := f'results/{now}_{args.tag}')
    os.mkdir(f'{results_dir}/csv')
    os.mkdir(f'{results_dir}/log')
    os.mkdir(f'{results_dir}/pdf')

    f_tests.initialize(results_dir)
    nf_tests.initialize(results_dir)

    if not check_testcase_labels(args.functional, f_tests.FUNCTIONAL_TESTS, 'functional'):
        exit(-1)
    if not check_testcase_labels(args.nonfunctional, nf_tests.NON_FUNCTIONAL_TESTS, 'non-functional'):
        exit(-1)

    run_test_subset(args.functional, f_tests.FUNCTIONAL_TESTS)
    run_test_subset(args.nonfunctional, nf_tests.NON_FUNCTIONAL_TESTS)

    if args.functional is None and args.nonfunctional is None:
        for tag in f_tests.FUNCTIONAL_TESTS.keys():
            f_tests.FUNCTIONAL_TESTS[tag].run(args.tag)
        for tag in nf_tests.NON_FUNCTIONAL_TESTS.keys():
            nf_tests.NON_FUNCTIONAL_TESTS[tag].run(args.tag)


def run_test_subset(passed_argument_tags, functional_tests):
    if passed_argument_tags is None:
        return

    if len(passed_argument_tags) > 0:
        for tag in passed_argument_tags:
            functional_tests[tag].run(args.tag)
        return

    for tag in functional_tests:
        functional_tests[tag].run(args.tag)


if __name__ == "__main__":
    main()
