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
        AUTH_URL = '{}/oauth/token'.format(config['gitlab']['base_url'])
        response = requests.post(AUTH_URL, data={
            'grant_type': 'password',
            'username': config['gitlab']['username'],
            'password': config['gitlab']['password']
        })

        token = response.json()['access_token']
        self.gl = Gitlab(config['gitlab']['base_url'], oauth_token=token)

    def verify_project_exists(self, name):
        projects = self.gl.projects.list()

        for project in projects:
            project.delete()

        sleep(1)
        self.gl.projects.create({'name': name})


class GitUtil:
    def __init__(self, git_url, tag=None):
        self.REPOPATH = config['git']['repopath']
        self.RESULTS_DIR = os.environ.get('RESULTS_DIR')
        try:
            shutil.rmtree(self.REPOPATH)
        except OSError as e:
            print(e)
        os.mkdir(self.REPOPATH)

        self.REPO = Repo.clone_from(git_url, self.REPOPATH)
        self.GIT = Git(self.REPOPATH)

        if tag:
            self.GIT.checkout(tag)

    def copy_file_into_repo(self, file):
        target = os.path.join(self.REPOPATH, os.path.basename(file))
        copyfile(file, target)
        self.REPO.index.add([os.path.basename(target)])

    def commit_and_push_source_code(self, message):
        self.REPO.index.commit(message)
        self.REPO.remotes.origin.push()

    def tag_repository(self, tag_name):
        tag = self.REPO.create_tag(tag_name)
        self.REPO.remotes.origin.push(tag)

    def purge_repository(self):
        shutil.rmtree(self.REPOPATH)
        os.mkdir(self.REPOPATH)

    def create_new_file(self, filename, content):
        target = os.path.join(self.REPOPATH, filename)
        with open(target, 'w') as file:
            file.writelines(content)
        self.REPO.index.add([os.path.basename(target)])

    def copy_repofile_to_results(self, filename, execution_tag):
        shutil.copyfile(os.path.join(self.REPOPATH, filename),
                        os.path.join(self.RESULTS_DIR, 'pdf', f"{execution_tag}_{filename}"))

    def replace_repofile(self, src, target):
        target=os.path.join(self.REPOPATH, target)
        os.remove(target)
        shutil.copyfile(src, target)

    def checkout(self, branch):
        self.GIT.checkout(branch)
