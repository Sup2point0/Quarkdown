'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import os
import base64

## NOTE testing
import github
with open("test-output.txt", "w") as file:
  file.write(", ".join(dir(github)))
##

from github import Auth
from github import Github

# import quarkdown


with Github(auth = Auth.Token(os.getenv("AQ"))) as git:

  ## setup
  repo = git.get_repo("Sup2point0/Assort")
  content = repo.get_contents("")

  docs = []
  files = []
  
  ## extract
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
  
  ## render, upload
  for file in files:
    text = base64.b64decode(file.content)
    print(text)
    # file = quarkdown.textualise(text)
    # path = f"docs/{file.path}.html"
  
    ## NOTE testing
    path = f"docs/test.txt"
    repo.create_file(path, "auto-assort", text)
    continue
    ##
  
    ## FIXME?
    try:
      existing = repo.get_contents(path)
      repo.update_file(path, "auto-assort", file.content, sha = existing.sha)
  
    except:
      repo.create_file(path, "auto-assort", file.content)
