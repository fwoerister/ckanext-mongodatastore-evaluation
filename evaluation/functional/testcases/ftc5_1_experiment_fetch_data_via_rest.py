import logging
from time import sleep

from evaluation.util import env, ckan
from evaluation.util.script import run_r_script
from evaluation.util.scv import GitlabUtil, GitUtil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logging.info("Start execution of 'tc5_1'")

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
# creatnamee subset

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

git_util.copy_file_into_repo('scripts/restapi/RR.R')
git_util.copy_file_into_repo('datasets/pid')
git_util.push_source_code()

run_r_script('RR.R')

git_util.tag_repository('1.0')

# todo: modify data
new_record = {'id': 1278, 'Country': 'Australia', 'Year': 2010, 'Debt': 101136.25205, 'RGDP': None, 'GDP': None,
              'dRGDP': 0.732249739168633, 'GDPI': 109.15168, 'GDP1': None, 'GDP2': 1201390, 'RGDP1': None,
              'RGDP2': 1100661, 'GDPI1': None, 'GDPI2': None, 'Infl': '1.629', 'Debt1': None, 'Debt2': None,
              'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': 8.41826984160015,
              'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': 1092660}
ckan.client.action.datastore_upsert(resource_id=resource_id, records=[new_record], method='insert', force=True)

new_record = {'id': 1, 'Country': 'Australia', 'Year': 2010, 'Debt': None, 'RGDP': None, 'GDP': None,
              'dRGDP': None, 'GDPI': None, 'GDP1': None, 'GDP2': None, 'RGDP1': None,
              'RGDP2': 1100661, 'GDPI1': None, 'GDPI2': None, 'Infl': None, 'Debt1': None, 'Debt2': None,
              'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': None,
              'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': None}

ckan.client.action.datastore_upsert(resource_id=resource_id, records=[new_record], method='upsert', force=True)

git_util.purge_repository()
git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git', '1.0')
run_r_script('RR.R')

# todo: modify code


git_util.purge_repository()
git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git', '1.0')
run_r_script('RR.R')

# EXPECTED RESULTS

# todo: check if results are same
