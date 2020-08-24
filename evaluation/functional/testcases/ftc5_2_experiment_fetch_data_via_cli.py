import logging
from time import sleep

from evaluation.util import env, ckan
from evaluation.util.script import run_bash_script
from evaluation.util.scv import GitlabUtil, GitUtil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logging.info("Start execution of 'tc5_2'")

gitlab_util = GitlabUtil()

# DESCRIPTION

# PRE-REQUISIT
env.verify_containers_are_running()
ckan.verify_package_does_exist('rr-experiment')
resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                    {'name': 'countries_dataset.csv', 'datastore_active': True})

gitlab_util.verify_project_exists('rr-experiment')

logging.info("pre-requisists are fullfilled")

# STEPS
# create subset

pid = ckan.client.action.issue_pid(resource_id=resource_id,
                                   filters={'Year': {'$gte': 1946}, 'Year': {'$lte': 2009},
                                            '$or': [{'Year': {'$not': {'$lt': 1951}}},
                                                    {'Country': {'$not': {'$eq': 'Italy'}}}]})

logger.info("wait 5 seconds for background job to finish...")
sleep(5)

response = ckan.client.action.querystore_resolve(pid=pid)
with open('datasets/pid', 'w') as f:
    f.writelines(response['query']['handle_pid'])

# publish source code to gitlab
git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git')

git_util.copy_file_into_repo('scripts/cli/RR.R')
git_util.copy_file_into_repo('scripts/cli/run_experiment.sh')
git_util.copy_file_into_repo('datasets/pid')
git_util.push_source_code()

run_bash_script('run_experiment.sh')

git_util.tag_repository('1.0')

# todo: modify data

# todo: modify code

# todo: re-checkout code in new folder

# todo: re-run

# EXPECTED RESULTS

# todo: check if results are same
