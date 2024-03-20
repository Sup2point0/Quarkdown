'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import os

from github import Github, Auth

import deploy


with Github(auth = Auth.Token(os.getenv("AQ"))) as git:
  repo = git.get_repo("Sup2point0/Assort")
  files = deploy.extract_repo_files(repo)
  log = deploy.export_and_deploy(git, repo, files, "auto-assort")
  deploy.update_logs(git, "Assort", log)
