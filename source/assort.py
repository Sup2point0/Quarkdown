'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import os
import base64

from github import GitHub
from github import Auth

import quarkdown


## setup
git = GitHub(auth = Auth.Token(os.getenv("STIG"))
repo = git.get_repo("Sup2point0/Assort")
content = repo.get_contents("")


## extract, sort
docs = []
files = []

while content:
  file = content.pop(0)

  if file.type == "dir":
    if not file.path.split("/")[-1].startswith("."):
      folder = repo.get_contents(file.path)
      content.extend(folder)

  elif file.path.lower().endswith(".md"):  ## NOTE lower needed?
    files.append(file)

  elif file.path.startswith("docs/"):
    docs.append(file.path)


## render, upload, commit
for file in files:
  text = base64.b64decode(file.content)
  print(text)
  file = quarkdown.textualise(text)
  path = f"docs/{file.path}.html"

  try:
    break  ## NOTE testing
    existing = repo.get_contents(path)
    repo.update_file(path, "auto-assort", file.content, sha = existing.sha)

  except:
    repo.create_file(path, "auto-assort", file.content)


git.close()
