'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import os
import time

from github import Github, Auth

# this is ugly, but it'll have to do until we find a workaround
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])

import quarkdown as qk
#

start = time.time()

key = os.getenv("CHARM")
if key is None:
  raise ValueError("no access key found!")

with Github(auth = Auth.Token(key)) as git:
  home, repo = qk.prepare_deploy(git, "Sup2point0/Quarkdown")

  files = qk.extract_repo_files(repo, "tests/")
  log_home, log_repo = qk.export_and_deploy(home, repo, files, commit = "#QUARK export file")

  qk.update_logs(home, "assort", log_repo)
  
  qk.finish(start, log_home)
  qk.update_logs(home, "quarkup", log_home)
