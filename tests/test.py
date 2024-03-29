'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import os

from github import Github, Auth

import quarkdown as qk


print(qk.process_quarks("<!-- #QUARK LIVE --> <!-- #QUARK \n EXPORT test/test --> test"))


# key = os.getenv("AQ")
# if key is None:
#   raise ValueError("no access key found!")

# with Github(auth = Auth.Token(key)) as git:
#   repo = git.get_repo("Sup2point0/Assort")
#   files = deploy.extract_repo_files(repo)
#   log = deploy.export_and_deploy(git, repo, files, commit = "auto-assort")
#   deploy.update_logs(git, "Assort", log)
