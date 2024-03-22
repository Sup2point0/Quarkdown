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

import quarkdown


def extract_repo_files(repo: Repository, path = "") -> list[ContentFile]:
  '''Extract all .md files from a GitHub repository.'''

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


def export_and_deploy(
  git: Github,
  repo: Repository,
  files: list[ContentFile],
  *,
  commit: str,
) -> dict:
  '''Export .md files to HTML and commit them to the `docs/` folder of a given GitHub repository.'''

  log = extract_logs(git, repo.name.lower())

  for file in files:
    if not has_changed(file, log):
      continue
    
    decoded: str = base64.b64decode(file.content).decode()

    try:
      text = quarkdown.textualise(decoded)
      export = quarkdown.export(text)
    except quarkdown.Quarkless:
      continue

    path = export["path"]
    content = export["content"]

    try:
      existing = repo.get_contents(path)
    except UnknownObjectException:
      repo.create_file(path, commit, content)
    else:
      repo.update_file(path, commit, content, existing.sha)

    # reduce Unix timestamp for easier management
    log[path] = {
      "export-path": path,
      "last-updated": round(time.time() % 1710000000),
    }

  return log


def has_changed(file: ContentFile, log: dict) -> bool:
  '''Check if a file has been updated since the last export and deployment.'''

  deployed = log.get(file.name.lower(), False)
  if not deployed:
    return True

  modified = round(file.last_modified_datetime.timestamp() % 1710000000)

  print(f"file {file.name} -> modified: {modified}, deployed: {deployed}")

  return modified - deployed > 0


def extract_logs(
  git: Github,
  repo_name: str,
) -> dict:
  '''Extract logs for a particular repository.'''

  repo = git.get_repo("Sup2point0/Quarkdown")
  file = repo.get_contents(f"source/logs/{repo_name.lower()}.json")
  text = base64.b64decode(file.content)

  return json.loads(text)


def update_logs(
  git: Github,
  repo_name: str,
  log: dict,
) -> None:
  '''Update logs for a particular repository.'''

  repo = git.get_repo("Sup2point0/Quarkdown")
  existing = repo.get_contents(f"source/logs/{repo_name.lower()}.json")

  repo.update_file(
    path = existing.path,
    message = f"#QUARK update logs for {repo_name}",
    content = json.dumps(log, indent = 2),
    sha = existing.sha,
  )
