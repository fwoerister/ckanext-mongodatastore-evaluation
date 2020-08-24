import json
import os
import shutil
from shutil import copyfile
from time import sleep

import requests
from git import Repo, Git
from gitlab import Gitlab

config = json.load(open('../config.json', 'r'))

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

    def push_source_code(self):
        for f in os.listdir(self.REPOPATH):
            if not f.startswith('.'):
                self.REPO.index.add([f])

        self.REPO.index.commit("source code added")
        self.REPO.remotes.origin.push()

    def tag_repository(self, tag_name):
        tag = self.REPO.create_tag(tag_name)
        self.REPO.remotes.origin.push(tag)

    def purge_repository(self):
        shutil.rmtree(self.REPOPATH)
        os.mkdir(self.REPOPATH)
