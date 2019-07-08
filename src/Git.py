import git

from git.exc import GitCommandError


class GitManager:

        def push(self, path):
                repo = self.createOrGetRepository(self, path)
                try:
                        repo.git.add('*.*')
                        repo.git.commit("-m test")

                except GitCommandError as e:
                        print(e)
                        pass

                repo.git.push("origin", "master")

        def pull(self, path):
                repo = self.createOrGetRepository(self, path)
                origin = repo.remote()
                origin.fetch()
                origin.pull()

        def createOrGetRepository(self, path):
                git.Repo.init(path)
                repo = git.Repo(path)
                try:
                        git.Remote.add(repo, "origin", "https://github.com/mimela98/origin.git")

                except GitCommandError as e:
                        print(e)
                        pass

                return repo
