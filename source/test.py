'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import base64
import os

from github import Github, Auth

import deploy


with Github(auth = Auth.Token(os.getenv("AQ"))) as git:

  ## setup
  repo = git.get_repo("Sup2point0/Assort")
  files = deploy.extract_repo_files(repo)
  test = repo.get_contents("docs/nonexistent.txt")
  raise NotImplementedError(test)
