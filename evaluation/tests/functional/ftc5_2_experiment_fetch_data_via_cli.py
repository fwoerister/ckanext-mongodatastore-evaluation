# DESCRIPTION

import logging
from time import sleep

from evaluation.tests import GenericFunctionalTest
from evaluation.util import ckan
from evaluation.util import env
from evaluation.util.script import run_bash_script
from evaluation.util.scv import GitlabUtil, GitUtil

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ExperimentCliFunctionalTest(GenericFunctionalTest):

    def __init__(self, results_dir, name):
        super(ExperimentCliFunctionalTest, self).__init__(results_dir, name)
        self.gitlab_util = GitlabUtil()
        self.log_hashes = []
        self._resource_id = None

    def _check_precondition(self):
        GitUtil.purge_repository()
        env.verify_containers_are_running()
        ckan.verify_package_does_exist('rr-experiment')
        self._resource_id = ckan.verify_package_contains_resource('rr-experiment',
                                                                  {'name': 'countries_dataset.csv',
                                                                   'datastore_active': True})

        self.gitlab_util.verify_project_exists('rr-experiment')

    def _execute_steps(self):
        pid = ckan.client.action.issue_pid(resource_id=self._resource_id,
                                           filters={'Year': {'$gte': 1946}, 'Year': {'$lte': 2009},
                                                    '$or': [{'Year': {'$not': {'$lt': 1951}}},
                                                            {'Country': {'$not': {'$eq': 'Italy'}}}]})

        logger.info("wait 5 seconds for background job to finish...")
        sleep(5)

        response = ckan.client.action.querystore_resolve(pid=pid)
        pid = response['query']['handle_pid']

        # publish source code to gitlab
        git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git',
                           results_dir=self.results_dir)

        git_util.copy_file_into_repo('data/scripts/cli/RR.R')
        git_util.copy_file_into_repo('data/scripts/cli/run_experiment.sh')
        git_util.create_new_file("pid", pid)
        git_util.commit_and_push_source_code('source code added')

        self.log_hashes.append(run_bash_script(self.results_dir, 'run_experiment.sh', 'cli-run1'))
        git_util.copy_repofile_to_results('Rplots.pdf', 'cli-run1')

        git_util.tag_repository('1.0')

        new_record = {'id': 1278, 'Country': 'Australia', 'Year': 2010, 'Debt': 101136.25205, 'RGDP': None, 'GDP': None,
                      'dRGDP': 0.732249739168633, 'GDPI': 109.15168, 'GDP1': None, 'GDP2': 1201390, 'RGDP1': None,
                      'RGDP2': 1100661, 'GDPI1': None, 'GDPI2': None, 'Infl': '1.629', 'Debt1': None, 'Debt2': None,
                      'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': 8.41826984160015,
                      'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': 1092660}
        ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=[new_record], method='insert',
                                            force=True)

        new_record = {'id': 1, 'Country': 'Australia', 'Year': 2011, 'Debt': None, 'RGDP': None, 'GDP': None,
                      'dRGDP': None, 'GDPI': None, 'GDP1': None, 'GDP2': None, 'RGDP1': None,
                      'RGDP2': 1100662, 'GDPI1': None, 'GDPI2': None, 'Infl': None, 'Debt1': None, 'Debt2': None,
                      'Debtalt': None, 'GDP2alt': None, 'GDPalt': None, 'RGDP2alt': None, 'debtgdp': None,
                      'GDP3': None, 'GNI': None, 'lRGDP': None, 'lRGDP1': None, 'lRGDP2': 1234}

        ckan.client.action.datastore_upsert(resource_id=self._resource_id, records=[new_record], method='upsert',
                                            force=True)

        git_util.purge_repository()
        git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git',
                           results_dir=self.results_dir, tag='1.0')
        self.log_hashes.append(run_bash_script(self.results_dir, 'run_experiment.sh', 'cli-run2'))
        git_util.copy_repofile_to_results('Rplots.pdf', 'cli-run2')

        git_util.checkout('master')
        git_util.replace_repofile('data/scripts/restapi/RR_modified.R', 'RR.R')
        git_util.commit_and_push_source_code("source code modified")

        git_util.purge_repository()
        git_util = GitUtil('http://root:gitlab_passwd@localhost:8081/root/rr-experiment.git',
                           results_dir=self.results_dir, tag='1.0')
        self.log_hashes.append(run_bash_script(self.results_dir, 'run_experiment.sh', 'cli-run3'))
        git_util.copy_repofile_to_results('Rplots.pdf', 'cli-run3')

    def _check_postcondition(self):
        assert all(hash == self.log_hashes[0] for hash in self.log_hashes)
        # todo check if pdf output is equal
