import os
import json
import base64
import urllib
import abc
from github import Github
from github.GithubException import GithubException
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from notebook.notebookapp import ContentsManager


class GitCommitHandler(IPythonHandler, ContentsManager):

    metaclass = abc.ABCMeta

    def error_and_return(self, dirname, reason):

        # send error
        self.send_error(500, reason=reason)

        # return to directory
        os.chdir(dirname)

    @abc.abstractmethod
    def put(self):

        # git vars
        g = Github(os.getenv("GIT_TOKEN"))
        branch = os.getenv("GIT_BRANCH_NAME")
        repo_name = "newellp2019/" + os.getenv("GIT_REPO")
        if branch:
            repo_branch = repo_name + "/" + branch
            repo = g.get_repo(repo_name)
        else:
            repo = g.get_repo(repo_name)

        cm = C()
        pushed_file = self.request.headers['Referer'].split("?")[0]
        print(pushed_file)
        pushed_file = self.get(pushed_file)
        print(pushed_file)

        # obtain filename and msg for commit
        data = json.loads(self.request.body.decode('utf-8'))
        content = self.request.files
        print(data, content, self.request.headers, self.request.host, self.request.arguments)
        print(self.request.headers)
        filename = urllib.parse.unquote(data['filename']).split("/")[1]
        msg = data['msg']
        self.process_commit(g, repo, filename, msg, branch)

    def process_commit(self, g, repo, new_file, msg, branch):
        try:
            contents = repo.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    if new_file == file_content.path:
                        self.update_file(g, msg, new_file, branch)
                    else:
                        self.create_file(g, msg, new_file, branch)
        except GithubException as ge:
            print(ge)
            self.create_file(repo, msg, new_file, branch)

    @staticmethod
    def update_file(repo, msg, new_file, branch):
        repo.update_file(new_file, msg, msg, branch=branch)

    @staticmethod
    def create_file(repo, msg, new_file, branch, data):
        print(msg, new_file, branch)
        repo.create_file(message=msg, content=base64.encode(msg), path=new_file, branch=branch)


def setup_handlers(nbapp):
    route_pattern = ujoin(nbapp.settings['base_url'], '/git/commit')
    nbapp.add_handlers('.*', [(route_pattern, GitCommitHandler)])
