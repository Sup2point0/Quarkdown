'''
Deploys .md files in a GitHub repo to GitHub Pages.
'''

import base64
import json
import time

from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile

import quarkdown


def extract_repo_files(repo: Repository) -> list[ContentFile]:
  '''Extract all .md files from a GitHub repository.'''

  out = []
  content = repo.get_contents("")

  while content:
    file = content.pop(0)

    if file.type == "dir":
      if not file.path.split("/")[-1].startswith("."):
        folder = repo.get_contents(file.path)
        content.extend(folder)
  
    elif file.path.endswith(".md"):
      out.append(file)

  return out


def export_and_deploy(
  git: Github,
  repo: Repository,
  files: list[ContentFile],
  *,
  commit: str,
) -> dict:
  '''Export .md files to HTML and commit them to the `docs/` folder of a given GitHub repository.'''

  log = extract_logs(git, repo.name)

  for file in files:
    text = base64.base64decode(file.content)
    path, content = quarkdown.textualise(text)

    try:
      repo.create_file(path, commit, content)
    except:
      existing = repo.get_contents(path)
      repo.update_file(path, commit, content, existing.sha)

    # reduce Unix timestamp for easier management
    log[path]["last-updated"] = round(time.now())# % 1710000000)

  return log


def has_changed(file: ContentFile, log: dict) -> bool:
  '''Check if a file has been updated since the last export and deployment.'''

  modified = round(file.last_modified_datetime.timestamp())
  deployed = log[file.name]

  print(f"modified: {modified}, deployed: {deployed}")

  return modified - deployed > 0


def extract_logs(
  git: Github,
  repo_name: str,
) -> dict:
  '''Extract logs for a particular repository.'''

  repo = git.get_repo("Sup2point0/Quarkdown")
  file = repo.get_contents(f"source/logs/{repo_name.lower()}.json")
  text = base64.base64decode(file.content)

  return json.loads(text)


def update_logs(
  git: Github,
  repo_name: str,
  log: dict,
) -> None:
  '''Update logs for a particular repository.'''

  repo = git.get_repo("Sup2point0/Quarkdown")
  existing = repo.get_contents(f"source/logs/{repo_name}.json")

  repo.update_file(
    path = existing.path,
    message = f"#QUARK update logs for {repo_name}",
    content = json.dumps(log, indent = 2),
    sha = existing.sha,
  )
