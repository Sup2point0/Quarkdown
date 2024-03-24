'''
Pipeline functions for processing text.
'''

import re

import requests


def clear_comments(text: str) -> str:
  '''Remove HTML comments from given text.'''

  return re.sub("<!--.*-->", "", text)


def textualise(text: str) -> str:
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
