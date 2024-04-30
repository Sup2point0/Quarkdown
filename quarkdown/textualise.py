'''
Pipeline functions for processing text.
'''

import re
import textwrap

import requests


def tokenise(token: dict, defaults: dict) -> dict:
  '''Fill in unspecified attributes of a token with their defaults.'''

  return {key: token.get(key, val) for key, val in defaults.items()}


def sanitise_filename(name: str) -> str:
  '''Format a file name to simple lowercase `kebab-case`.'''

  return name.lower().replace(" ", "-")


def render_html(text: str) -> str:
  '''Render Github-Flavoured Markdown to HTML through the GitHub API.'''

  response = requests.post(
    "https://api.github.com/markdown",
    json = {
      "mode": "markdown",
      "text": text,
    },
  )

  if response.status_code == 200:
    return response.text
  else:
    raise FileNotFoundError("#QUARK failed to access Github-Flavoured Markdown API")


def clear_comments(text: str) -> str:
  '''Remove HTML comments from given text.'''

  return re.sub("<!--.*-->", "", text)


def indent(text: str, spaces: int) -> str:
  '''Add indentation to multi-line text.'''

  return textwrap.indent(text, " " * spaces)
