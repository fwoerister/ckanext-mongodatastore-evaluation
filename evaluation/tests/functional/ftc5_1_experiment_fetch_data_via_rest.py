import os
from time import sleep

from evaluation.tests import GenericFunctionalTest
from evaluation.tests.functional.static_test_assets import PACKAGE, RESOURCE_FILE_LOCATION, SUBSET_QUERY
from evaluation.util import ckan, handle
from evaluation.util.script import run_r_script
from evaluation.util.scv import GitlabUtil, GitUtil


class ExperimentRestFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(ExperimentRestFunctionalTest, self).__init__(results_dir, name)
        self.gitlab_util = GitlabUtil()
        self.log_hashes = []
        self._resource_id = None

    def _check_precondition(self):
        os.makedirs('gitrepository', exist_ok=True)

        GitUtil.purge_repository()
        self._resource_id = ckan.reset_package_to_initial_state(PACKAGE, RESOURCE_FILE_LOCATION)

        ckan.ensure_package_does_not_exist('rr-experiment')
        self.gitlab_util.verify_project_exists('rr-experiment')

    def _execute_steps(self):
        # 1) Issue a pid for SUBSET query
        self.logger.info("issue pid for data subset...")
        pid = ckan.client.action.issue_pid(resource_id=self._resource_id,
                                           filters=SUBSET_QUERY)

        self.logger.info("wait 5 seconds for background job to finish...")
        sleep(5)

        response = ckan.client.action.querystore_resolve(id=pid)
        pid = response['query']['handle_pid']

        # 2) push source code to gitlab
        self.logger.info("push experiment source code to gitlab...")
        git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git',
                           results_dir=self.results_dir)
        git_util.copy_file_into_repo('data/scripts/restapi/RR.R')
        git_util.commit_and_push_source_code("source code added")

        # 3) Attache Subset PID to Experiment
        self.logger.info("add pid to gitlab repository...")
        git_util.create_new_file("pid", pid)
        git_util.commit_and_push_source_code("pid file added")

        # 4) Tag current version as 1.0
        self.logger.info("tag current repository version as '1.0'...")
        git_util.tag_repository('1.0')

        code_pid = handle.client.put_handle_for_urls(
            {'URL': 'http://gitlab:8081/root/rr-experiment/-/archive/1.0/rr-experiment-1.0.zip'}
        ).json().get('handle')

        # 5) Run the experiment + 6) Calculate a md5 hash value of the results
        self.logger.info("re-execute experiment and calculate hash of result...")
        self.log_hashes.append(run_r_script(self.results_dir, 'RR.R', 'rest-run1'))
        git_util.copy_repofile_to_results('Rplots.pdf', 'rest-run1')

        # 7) Create experiment dataset in CKAN, containing Code, Datasubset and Paper
        self.logger.info("publish experiment in ckan repository...")
        package = ckan.client.action.package_create(name='rr-experiment', title='Reinhard&Rogoff Experiment',
                                                    private=False,
                                                    owner_org='tu-wien',
                                                    author='Carmen Reinhart; Kenneth Rogoff',
                                                    maintainer='', license='other-open',
                                                    extras=[{'key': 'year', 'value': '2010'}])

        ckan.client.action.resource_create(package_id=package['id'],
                                           name='post-war-datasubset',
                                           url=f'https://localhost:8000/{pid}',
                                           format='pid')

        ckan.client.action.resource_create(package_id=package['id'],
                                           name='Does High Public Debt Consistently Stifle Economic Growth? A Critique of Reinhart and Rogoff',
                                           upload=open('data/datasets/paper.pdf', 'rb'),
                                           format='pdf')

        ckan.client.action.resource_create(package_id=package['id'],
                                           name='Experiment Source Code',
                                           url=f'http://handle_server:8000/{code_pid}',
                                           format='zip')

        # 8) Modify the dataset in the CKAN repository
        self.logger.info("modify parent dataset...")
        new_record = {'id': 1278, 'Country': 'Australia', 'Year': 2010, 'Debt': 101136.25205, 'RGDP': None, 'GDP': None,
                      'dRGDP': 0.732249739168633, 'GDPI': 109.15168, 'GDP1': None, 'GDP2': 1201390, 'RGDP1': None,
                      'RGDP2': 1100661, 'GDPI1': None, 'GDPI2': None, 'Infl': '1.629', 'Debt1': None, 'Debt2': None,
                      'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': 8.41826984160015,
                      'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': 1092660}
        ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=[new_record], method='insert',
                                            force=True)

        new_record = {'id': 1, 'Country': 'Australia', 'Year': 2010, 'Debt': None, 'RGDP': None, 'GDP': None,
                      'dRGDP': None, 'GDPI': None, 'GDP1': None, 'GDP2': None, 'RGDP1': None,
                      'RGDP2': 1100661, 'GDPI1': None, 'GDPI2': None, 'Infl': None, 'Debt1': None, 'Debt2': None,
                      'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': None,
                      'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': None}

        ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=[new_record], method='upsert',
                                            force=True)

        # 9) re-run experiment + 10) calculate hash of result
        self.logger.info("re-execute experiment and calculate hash of result...")
        self.log_hashes.append(run_r_script(self.results_dir, 'RR.R', 'rest-run2'))
        git_util.copy_repofile_to_results('Rplots.pdf', 'rest-run2')

        # 10) Purge repository
        self.logger.info("purge local repository...")
        git_util.purge_repository()

        # 11) Modify source code
        self.logger.info("modify source code...")
        git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git',
                           results_dir=self.results_dir, tag='1.0')
        git_util.checkout('master')
        git_util.replace_repofile('data/scripts/restapi/RR_modified.R', 'RR.R')
        git_util.commit_and_push_source_code("source code modified")

        git_util.purge_repository()

        # 12) Checkout version 1.0
        self.logger.info("checkout tag '1.0' of experiment repository...")
        git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git',
                           results_dir=self.results_dir, tag='1.0')

        # 13) re-run experiment + 14) calculate hash of result
        self.logger.info("re-execute experiment and calculate hash of result...")
        self.log_hashes.append(run_r_script(self.results_dir, 'RR.R', 'rest-run3'))
        git_util.copy_repofile_to_results('Rplots.pdf', 'rest-run3')

    def _check_postcondition(self):
        assert all(hash == self.log_hashes[0] for hash in self.log_hashes)
