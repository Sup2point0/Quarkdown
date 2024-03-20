'''
Deploys .md files in a GitHub repo to GitHub Pages.
'''

import time
import base64

from github import Repository, ContentFile

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
  repo: Repository,
  files: list[ContentFile],
  *,
  commit: str,
) -> None:
  '''Export .md files to HTML and commit them to the `docs/` folder of a given GitHub repository.'''

  log = extract_log(repo.name)

  for file in files:
    text = base64decode(file.content)
    path, content = quarkdown.textualise(text)

    try:
      repo.create_file(path, commit, content)
    except:
      existing = repo.get_contents(path)
      repo.update_file(path, commit, content, existing.sha)

    # reduce Unix timestamp for easier management
    log[path]["last-updated"] = round(time.now() % 1710000000)


def has_changed(file: ContentFile, log: dict) -> bool:
  '''Check if a file has been updated since the last export and deployment.'''


def extract_log(git: Github, name: str) -> dict:
  '''Extract a log file for a particular repo.'''

  repo = git.get_repo(f"Sup2point0/Quarkdown")
  file = repo.get_contents("source/logs/{name}.json")
  text = str(base64decode(file.content))

  return json.loads(content.)


def update_log(file: ContentFile):
  '''Update deploy logs to track if files need to be updated.'''

  raise NotImplementedError()
