import os, sys
import wasanbon
from wasanbon.util import git, github_ref
from wasanbon.core.rtc import repository

class RTnoProjectObject:
    def __init__(self, root, file):
        self._path = root
        self._file = os.path.join(root, file)

    @property
    def name(self):
        return os.path.basename(self._path)

    @property
    def path(self):
        return self._path

    @property
    def file(self):
        return self._file

    def git_init(self, verbose=False):
        git_obj = wasanbon.util.git.GitRepository(self.path, init=True, verbose=verbose)
        git_obj.add(['.'], verbose=verbose)
        git_obj.add(['.project', '.gitignore'], verbose=verbose)
        first_comment = 'This if first commit. This repository is generated by wasanbon'    
        git_obj.commit(first_comment, verbose=verbose)
        return self.git

    def github_init(self, user, passwd, verbose=False):
        github_obj = github_ref.GithubReference(user, passwd)
        repo = github_obj.create_repo(self.name)
        git.git_command(['remote', 'add', 'origin', 'git@github.com:' + user + '/' + self.name + '.git'], verbose=verbose, path=self.path)
        git.git_command(['push', '-u', 'origin', 'master'], verbose=verbose, path=self.path)    
        return self

    @property
    def git(self):
        return git.GitRepository(self.path)

    @property
    def repository(self):
        git_obj = wasanbon.util.git.GitRepository(self.path)
        return repository.RtcRepository(self.name, url=git_obj.url, desc="", hash=git_obj.hash)
