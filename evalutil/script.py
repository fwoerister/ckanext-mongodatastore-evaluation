import json
import os
from datetime import datetime
from subprocess import run

import evalutil.hash as hash

RESULT_DIR = os.environ.get('RESULTS_DIR')
EXPERIMENT_LOG_HASHES = 'experiment_log_hashes.csv'

config = json.load(open('config.json', 'r'))


def _get_log_file(filepath, execution_name):
    now = int(datetime.now().timestamp())
    stdout = open(os.path.join(RESULT_DIR, 'log', f'{now}_{execution_name}.log'), 'w')

    if execution_name is None:
        execution_name = os.path.basename(filepath)

    return open(os.path.join(RESULT_DIR, 'log', f'{now}_{execution_name}.log'), 'w')


def run_r_script(file, execution_name=None):
    cmd = ['Rscript', file]
    logfile = _get_log_file(file, execution_name)
    run(cmd, cwd=config['git']['repopath'], stdout=logfile, stderr=logfile)
    logfile.close()
    log_hash = hash.calculate_hash_of_file(logfile.name)
    with open(os.path.join(RESULT_DIR, 'csv', EXPERIMENT_LOG_HASHES), 'a') as hash_file:
        hash_file.writelines(f"{os.path.basename(logfile.name)};{log_hash}\n")

    return log_hash


def run_bash_script(file, execution_name=None, calculate_hash=True):
    cmd = ['/bin/bash', file]
    logfile = _get_log_file(file, execution_name)

    run(cmd, cwd=config['git']['repopath'], stdout=logfile, stderr=logfile)

    logfile.close()
    log_hash=hash.calculate_hash_of_file(logfile.name)

    with open(os.path.join(RESULT_DIR, 'csv', EXPERIMENT_LOG_HASHES), 'a') as hash_file:
        hash_file.writelines(f"{os.path.basename(logfile.name)};{hash.calculate_hash_of_file(logfile.name)}\n")

    return log_hash
