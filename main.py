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
parser.add_argument('--functional', type=str, nargs='+', help=f'Available tests: ')
parser.add_argument('--nonfunctional', type=str, nargs='+')
args = parser.parse_args()


def main():
    now = int(datetime.now().timestamp())
    os.mkdir(results_dir := f'results/{now}_{args.tag}')
    os.mkdir(f'{results_dir}/csv')
    os.mkdir(f'{results_dir}/log')
    os.mkdir(f'{results_dir}/pdf')

    functional_tests = f_tests.initialize(results_dir)
    nonfunctional_tests = nf_tests.initialize(results_dir)

    if args.functional:
        for tag in args.functional:
            functional_tests[tag].run()
    elif args.nonfunctional is None:
        for tag in functional_tests.keys():
            functional_tests[tag].run()

    if args.nonfunctional:
        for tag in args.nonfunctional:
            nonfunctional_tests[tag].run()
    elif args.functional is None:
        for tag in nonfunctional_tests.keys():
            nonfunctional_tests[tag].run()


if __name__ == "__main__":
    main()
