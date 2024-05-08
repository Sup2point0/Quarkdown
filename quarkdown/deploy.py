'''
Deploys .md files in a GitHub repository to GitHub Pages.
'''

import base64
import json
import time
from datetime import datetime

from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException

from . import quarkify
from .classes import ExportFile, Quarkless, IsIndex
from .__version__ import __version__


EPOCH_OFFSET = 1710000000
'''Offset to reduce Unix timestamp by for easier management.'''


def prepare_deploy(git: Github, repo_name: str) -> tuple[Repository, Repository]:
  '''Prepar the quarkup process by accessing the home and target repositories.'''

  return (
    git.get_repo("Sup2point0/Quarkdown"),
    git.get_repo(repo_name),
  )


def finish(start: int, log: dict):
  '''Track how long the quarkup process took.'''

  latest = log[0]
  latest["duration"] = round(time.time() - start)
  latest["average"] = round(latest["duration"] / latest["changes"], 1)


def extract_repo_files(repo: Repository, path = "") -> list[ContentFile]:
  '''Extract all .md files from directory `path` of a repository.'''

  out = []
  content = repo.get_contents(path)

  while content:
    file = content.pop(0)

    if file.type == "dir":
      if not file.path.split("/")[-1].startswith("."):
        folder = repo.get_contents(file.path)
        content.extend(folder)
  
    elif file.path.endswith(".md"):
      out.append(ExportFile(file = file))

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
  repo_config: dict = {},
) -> dict:
  '''Export .md files to HTML and commit them to the `docs/` folder of a given GitHub repository. Returns a `dict` log of changed files.'''

  log_home = extract_repo_json(home, f"quarkdown/logs/quarkup.json")
  log_repo = extract_repo_json(home, f"quarkdown/logs/{repo.name.lower()}.json")

  log_home.insert(0, {
    "run": len(log_home), 
    "epox": round(time.time() - EPOCH_OFFSET),
    "date": datetime.now().strftime("%y-%m-%d"),
    "changes": 0,
    "duration": None,
    "average": None,
    "data": [],
  })

  index_pages = []
  indexed_pages = {}

  for file in files:
    if not has_changed(file, log_repo):
      continue

    try:
      export = quarkify.render(file, repo_config)  ### TODO track repo data
    except Quarkless:
      continue
    except IsIndex:
      index_pages.append(file)
      continue

    try:
      existing = repo.get_contents(export.path)
    except UnknownObjectException:
      repo.create_file(export.path, commit, export.content)
    else:
      repo.update_file(export.path, commit, export.content, existing.sha)

    for each in export.indexes or []:
      try:
        indexed_pages[each.casefold()].append(export)
      except KeyError:
        indexed_pages[each.casefold()] = [export]

    log_home[0]["changes"] += 1
    log_home[0]["data"].append(export.export_dict())

    log_repo[file.path] = {
      "version": __version__,
      "export-path": export.path,
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
    message = commit or f"#QUARK update logs",
    content = json.dumps(data, indent = 2),
    sha = existing.sha,
  )


def has_changed(file: ContentFile, log: dict) -> bool:
  '''Check if a file has been updated since the last export and deployment.'''

  existing = log.get(file.path, False)
  if not existing:
    return True
  
  if existing["version"] != __version__:
    return True
  
  deployed = existing["last-export"]
  modified = round(file.last_modified_datetime.timestamp() - EPOCH_OFFSET)

  return modified - deployed > 0
