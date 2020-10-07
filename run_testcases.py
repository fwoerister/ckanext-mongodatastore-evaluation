import argparse
import hashlib
import logging
import os
import random
import shutil
import urllib.request
import zipfile
from datetime import datetime

from pyzenodo3 import Zenodo

import evaluation.tests.functional as f_tests
import evaluation.tests.nonfunctional as nf_tests

random.seed(4491)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TRACE_TEST_ASSETS_DOI = '10.5281/zenodo.4058379'
REINHART_AND_ROGOFF_TEST_ASSETS_DOI = '10.5281/zenodo.4072334'

parser = argparse.ArgumentParser(description='Run the evaluation experiments of the ckanext-mongodatastore project')
parser.add_argument('tag', type=str, help='A tag that is included in the name of the results folder')
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


def run_test_subset(passed_argument_tags, functional_tests):
    if passed_argument_tags is None:
        return

    if len(passed_argument_tags) > 0:
        for tag in passed_argument_tags:
            functional_tests[tag].run(args.tag)
        return

    for tag in functional_tests:
        functional_tests[tag].run(args.tag)


def retrieve_test_assets(doi, asset_targets):
    deposit = Zenodo().find_record_by_doi(doi).data

    for file in deposit.get('files'):
        if file['key'] in asset_targets.keys():
            target_locations = asset_targets[file['key']]

            if type(target_locations) == str:
                target_locations = [target_locations]

            for target_location in target_locations:
                if not is_file_valid(target_location, file['checksum'].split(':')[1], file['checksum'].split(':')[0]):
                    logger.info(f'Downloading the file "{file["key"]}" to the target location "{target_location}" ...')
                    urllib.request.urlretrieve(file['links']['self'], target_location)
                    logger.info('Download finished!')
                else:
                    logger.info(f'Download of file "{file["key"]}" was skipped. '
                                f'A identical file already exists in the target location!')


def is_file_valid(file, hash, hash_algo):
    if not os.path.exists(file):
        return False

    hash_md5 = hashlib.new(hash_algo)
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash == hash_md5.hexdigest()


def extract_archive(archive, target):
    archive_name = os.path.basename(archive).split('.')[0]

    shutil.rmtree(os.path.join(target, archive_name), ignore_errors=True)
    os.mkdir(os.path.join(target, archive_name))
    with zipfile.ZipFile(archive, 'r') as zip_file:
        zip_file.extractall(target)


def main():
    now = int(datetime.now().timestamp())
    os.mkdir(results_dir := f'results/{now}_{args.tag}')
    os.mkdir(f'{results_dir}/csv')
    os.mkdir(f'{results_dir}/log')
    os.mkdir(f'{results_dir}/pdf')

    os.makedirs('data/datasets', exist_ok=True)
    os.makedirs('data/scripts/cli', exist_ok=True)
    os.makedirs('data/scripts/restapi', exist_ok=True)

    retrieve_test_assets(TRACE_TEST_ASSETS_DOI, {
        'preprocessed_trace': 'data/datasets/preprocessed_trace',
        'preprocessed_trace_10000': 'data/datasets/preprocessed_trace_10000',
        'preprocessed_trace_100000': 'data/datasets/preprocessed_trace_100000',
        'preprocessed_trace_1000000': 'data/datasets/preprocessed_trace_1000000',
        'preprocessed_trace_remaining': 'data/datasets/preprocessed_trace_remaining',
        'trace_fields.json': 'data/datasets/trace_fields.json',
        'filter_values.zip': 'data/datasets/filter_values.zip'
    })

    extract_archive('data/datasets/filter_values.zip', 'data/datasets')

    retrieve_test_assets(REINHART_AND_ROGOFF_TEST_ASSETS_DOI, {
        'countries_dataset.csv': 'data/datasets/countries_dataset.csv',
        'paper.pdf': 'data/datasets/paper.pdf',
        'RR_cli.R': 'data/scripts/cli/RR.R',
        'RR_modified.R': ['data/scripts/cli/RR_modified.R', 'data/scripts/restapi/RR_modified.R'],
        'run_experiment.sh': 'data/scripts/cli/run_experiment.sh',
        'RR_rest.R': 'data/scripts/restapi/RR.R'
    })

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


if __name__ == "__main__":
    main()
