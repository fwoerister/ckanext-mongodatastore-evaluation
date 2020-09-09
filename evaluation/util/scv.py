import json
import os
import shutil
from shutil import copyfile
from time import sleep

import requests
from git import Repo, Git
from gitlab import Gitlab

config = json.load(open('config.json', 'r'))

REPO = None
GIT = Git(config['git']['repopath'])


class GitlabUtil():
    def __init__(self):
        self.AUTH_URL = '{}/oauth/token'.format(config['gitlab']['base_url'])
        self.gl = None

    def __init_client(self):
        response = requests.post(self.AUTH_URL, data={
            'grant_type': 'password',
            'username': config['gitlab']['username'],
            'password': config['gitlab']['password']
        })

        token = response.json()['access_token']
        self.gl = Gitlab(config['gitlab']['base_url'], oauth_token=token)

    def verify_project_exists(self, name):
        if self.gl is None:
            self.__init_client()
            
        projects = self.gl.projects.list()

        for project in projects:
            project.delete()

        sleep(1)
        self.gl.projects.create({'name': name})


class GitUtil:
    def __init__(self, git_url, results_dir=None, tag=None):
        self._repopath = config['git']['repopath']
        self._results_dir = results_dir
        try:
            shutil.rmtree(self._repopath)
        except OSError as e:
            print(e)
        os.mkdir(self._repopath)

        self.REPO = Repo.clone_from(git_url, self._repopath)
        self.GIT = Git(self._repopath)

        if tag:
            self.GIT.checkout(tag)

    @staticmethod
    def purge_repository():
        shutil.rmtree(config['git']['repopath'])
        os.mkdir(config['git']['repopath'])

    def copy_file_into_repo(self, file):
        target = os.path.join(self._repopath, os.path.basename(file))
        copyfile(file, target)
        self.REPO.index.add([os.path.basename(target)])

    def commit_and_push_source_code(self, message):
        self.REPO.index.commit(message)
        self.REPO.remotes.origin.push()

    def tag_repository(self, tag_name):
        tag = self.REPO.create_tag(tag_name)
        self.REPO.remotes.origin.push(tag)

    def create_new_file(self, filename, content):
        target = os.path.join(self._repopath, filename)
        with open(target, 'w') as file:
            file.writelines(content)
        self.REPO.index.add([os.path.basename(target)])

    def copy_repofile_to_results(self, filename, execution_tag):
        shutil.copyfile(os.path.join(self._repopath, filename),
                        os.path.join(self._results_dir, 'pdf', f"{execution_tag}_{filename}"))

    def replace_repofile(self, src, target):
        target = os.path.join(self._repopath, target)
        os.remove(target)
        shutil.copyfile(src, target)

    def checkout(self, branch):
        self.GIT.checkout(branch)
