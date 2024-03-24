'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

print(f"CURRENT PATH IS {__file__}")

import os

from github import Github, Auth

from .. import quarkdown as qk


key = os.getenv("CHARM")
if key is None:
  raise ValueError("no access key found!")

with Github(auth = Auth.Token(key)) as git:
  repo = git.get_repo("Sup2point0/Assort")
  files = qk.extract_repo_files(repo)
  log = qk.export_and_deploy(git, repo, files, commit = "auto-assort")
  print(log)
  qk.update_logs(git, "Assort", log)
