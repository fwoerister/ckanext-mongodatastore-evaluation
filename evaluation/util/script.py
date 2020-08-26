import json
import os
from datetime import datetime
from subprocess import run

import evaluation.util.hash as hash

EXPERIMENT_LOG_HASHES = 'experiment_log_hashes.csv'

config = json.load(open('config.json', 'r'))


def _get_log_file(results_dir, filepath, execution_name):
    now = int(datetime.now().timestamp())

    if execution_name is None:
        execution_name = os.path.basename(filepath)

    return open(os.path.join(results_dir, 'log', f'{now}_{execution_name}.log'), 'w')


def run_r_script(results_dir, file, execution_name):
    cmd = ['Rscript', file]
    logfile = _get_log_file(results_dir, file, execution_name)
    run(cmd, cwd=config['git']['repopath'], stdout=logfile, stderr=logfile)
    logfile.close()
    log_hash = hash.calculate_hash_of_file(logfile.name)
    with open(os.path.join(results_dir, 'csv', EXPERIMENT_LOG_HASHES), 'a') as hash_file:
        hash_file.writelines(f"{os.path.basename(logfile.name)};{log_hash}\n")

    return log_hash


def run_bash_script(results_dir, file, execution_name):
    cmd = ['/bin/bash', file]
    logfile = _get_log_file(results_dir, file, execution_name)

    run(cmd, cwd=config['git']['repopath'], stdout=logfile, stderr=logfile)

    logfile.close()
    log_hash = hash.calculate_hash_of_file(logfile.name)

    with open(os.path.join(results_dir, 'csv', EXPERIMENT_LOG_HASHES), 'a') as hash_file:
        hash_file.writelines(f"{os.path.basename(logfile.name)};{hash.calculate_hash_of_file(logfile.name)}\n")

    return log_hash
