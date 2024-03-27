'''
Deploys .md files in a GitHub repository to GitHub Pages.
'''

import base64
import json
import time

from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException

from . import quarkify


EPOCH_OFFSET = 1710000000
'''Offset to reduce Unix timestamp by for easier management.'''


def prepare_deploy(git: Github, repo_name: str) -> tuple[Repository, Repository]:
  '''Prepares the deployment process by accessing the home and target repositories.'''

  return (
    git.get_repo("Sup2point0/Quarkdown"),
    git.get_repo(repo_name),
  )


def extract_repo_files(repo: Repository, path = "") -> list[ContentFile]:
  '''Extract all .md files from the `path` directory of a repository.'''

  out = []
  content = repo.get_contents(path)

  while content:
    file = content.pop(0)

    if file.type == "dir":
      if not file.path.split("/")[-1].startswith("."):
        folder = repo.get_contents(file.path)
        content.extend(folder)
  
    elif file.path.endswith(".md"):
      out.append(file)

  return out


def extract_repo_json(repo: Repository, path = "") -> dict | list:
  '''Extract a specific .json file from a GitHub repository.'''

  file = repo.get_contents(path)
  text = base64.b64decode(file.content)
  data = json.loads(text)

  return data


def export_and_deploy(
  home: Repository,
  repo: Repository,
  files: list[ContentFile],
  *,
  commit: str,
) -> dict:
  '''Export .md files to HTML and commit them to the `docs/` folder of a given GitHub repository. Returns a `dict` log of changed files.'''

  log_home = extract_repo_json(home, f"quarkdown/logs/log.json")
  log_repo = extract_repo_json(home, f"quarkdown/logs/{repo.name.lower()}.json")

  log_home.insert(0, {
    "run": len(log_repo), 
    "epox": round(time.time() - EPOCH_OFFSET),
    "changes": 0,
    "data": [],
  })

  for file in files:
    if not has_changed(file, log_repo):
      continue
    
    text = base64.b64decode(file.content).decode()

    try:
      export = quarkify.export(text)
      path = export["path"]
    except quarkify.Quarkless:
      continue

    try:
      existing = repo.get_contents(path)
    except UnknownObjectException:
      repo.create_file(path, commit, export["content"])
    else:
      repo.update_file(path, commit, export["content"], existing.sha)

    log_home[0]["changes"] += 1
    log_home[0]["data"].append({"path": file.path, **export})

    log_repo[file.path.lower()] = {
      "export-path": path,
      "last-export": round(time.time() - EPOCH_OFFSET),
    }

  return log_home, log_repo


def update_logs(
  home: Repository,
  path: str,
  data: dict,
  *,
  commit: str = None,
):
  '''Update a .json log file in the Quarkdown repository.'''

  existing = home.get_contents(f"quarkdown/logs/{path}.json")

  home.update_file(
    existing.path,
    message = commit or f"#QUARK update logs for {path}",
    content = json.dumps(data, indent = 2),
    sha = existing.sha,
  )


def has_changed(file: ContentFile, log: dict) -> bool:
  '''Check if a file has been updated since the last export and deployment.'''

  existing = log.get(file.path.lower(), False)
  if not existing:
    return True
  
  deployed = existing["last-export"]
  modified = round(file.last_modified_datetime.timestamp() - EPOCH_OFFSET)

  return modified - deployed > 0
