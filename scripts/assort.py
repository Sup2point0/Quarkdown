'''
Script for GitHub Actions that deploys Markdown files in Assort to GitHub Pages.
'''

import base64
import os

from github import Github, Auth

from source import quarkdown


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
  
  ## process
  for file in files:

    ## render
    text = base64.b64decode(file.content)
    # file = quarkdown.textualise(text)
    path = f"docs/{file.path}.html"
  
    ## NOTE testing
    path = f"docs/test.txt"
    from datetime import datetime
    text = str(datetime.now()) + text
    try:
      existing = repo.get_contents(path)
      repo.update_file(path, "auto-assort", text, sha = existing.sha)
    except:
      repo.create_file(path, "auto-assort", text)
    
    break
    ##

    ## upload
    try:
      existing = repo.get_contents(path)
      repo.update_file(path, "auto-assort", file.content, sha = existing.sha)
  
    except:
      repo.create_file(path, "auto-assort", file.content)
