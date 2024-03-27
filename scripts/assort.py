'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import os

from github import Github, Auth

# this is ugly, but it'll have to do until we find a workaround
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])

import quarkdown as qk
#

key = os.getenv("CHARM")
if key is None:
  raise ValueError("no access key found!")

with Github(auth = Auth.Token(key)) as git:
  home, repo = qk.prepare_deploy(git, "Sup2point0/Assort")

  files = qk.extract_repo_files(repo)
  log_home, log_repo = qk.export_and_deploy(git, repo, files, commit = "auto-assort")

  qk.update_logs(home, "logs", log_home)
  qk.update_logs(home, "assort", log_repo)
