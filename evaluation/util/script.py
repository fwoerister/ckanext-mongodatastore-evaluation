import json
from subprocess import run

config = json.load(open('../config.json', 'r'))


def run_r_script(file):
    cmd = ['Rscript', file]
    run(cmd, cwd=config['git']['repopath'])


def run_bash_script(file):
    cmd = ['/bin/bash', file]
    run(cmd, cwd=config['git']['repopath'])
