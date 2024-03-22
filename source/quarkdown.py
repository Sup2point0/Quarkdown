'''
Quarkdown
v1.0.0
Markdown to HTML renderer
by Sup#2.0 (@Sup2point0)
available on GitHub: <https://github.com/Sup2point0/Quarkdown>
'''

import json
import re

from collections import namedtuple
from io import StringIO

import requests

import render


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK LIVE` flag.'''

  pass


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


def export(text: str) -> dict:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  # TODO this is a bit inefficient, we should find a better way to do this
  if "#QUARK LIVE" not in source:
    raise Quarkless("#QUARK file inactive")

  with open("tokens.json") as file:
    tokens = json.load(file)

  content = StringIO()
  context = []
  flags = {}

  # TODO do we process by line or in one single pass?
  for i, line in enumerate(source.split("\n")):
    for token in tokens["line"]:
      pass
    
    # for idx, string in enumerate(re.split("(\W)", line)):
    for idx, string in enumerate(line.split(" ")):
      for token in tokens:

        if _should_skip_(context, token):
          continue

        # skip processing if currently under HTML context
        if context[-1].kind == "html":
          continue

        # using try-except to reduce any more excessive indentation than there already is!
        try:
          # if info["idx"] is not None:
          #   assert idx == info["idx"]

          # pattern = info["re.open"]
          # if pattern is None:
          #   pattern = r"\n"

          # match = re.search(pattern, string)
          # assert match is not None

          # if info["ctx.kind"] is None:
          #   suf = info["re.close"]
          # else:
          #   suf = None
          #   context.append({
          #     "id": info["ctx.id"],
          #     "kind": info["ctx.kind"],
          #     "persist": info["ctx.persist"]
          #   })

          # pre = info["html.open"]
          # assert pre is not None
          # if not pre.startswith("<"):
          #   pre = f"<div class="{tag}">"
          # content.write(f"{pre}{string}{suf}")

          break

        except AssertionError:
          pass

        # close context
        try:
          # assert context[-1]["ctx"] == info["ctx"]

          # pattern = info["re.close"]
          # assert pattern is not None
          # match = re.search(pattern, string)
          # assert match is not None

          # context.pop()

          # suf = info["html.close"]
          # if suf is None:
          #   suf = "</div>"
          # content.write(f"{string}{suf}")

          break

        except AssertionError:
          pass

    while context[-1].done():
      context.pop()

    content.write(line + "\n")

  return {
    "content": content.value,
    "flags": flags,
  }


def _should_skip_(ctx, token) -> bool:
  '''Check if processing for a token should be skipped (when activation requisites are not fulfilled).'''

  if token["required-ctx"]:
    if ctx[-1].shard != token["required-ctx"]:
      return True

  if token["ctx-clashes"]:
    if ctx[-1].shard in token["ctx-clashes"]:
      return True
