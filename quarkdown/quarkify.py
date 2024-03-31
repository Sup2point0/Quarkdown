'''
Implements the Quarkdown parsing engine.
'''

import base64
import json
import os
import re

from github.ContentFile import ContentFile

from . import textualise
from .__version__ import __version__


__all__ = ["export"]


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK LIVE` flag.'''
  pass

class ContextOpened(Exception):
  '''Exception raised when a context has been successfully activated.'''
  pass


def export(file: ContentFile) -> dict:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  text = base64.b64decode(file.content).decode()
  
  load = extract_quarks(text)
  content = load["content"]
  content = textualise.render_html(content)
  content = textualise.clear_comments(content)

  root = os.path.split(os.path.abspath(__file__))[0]
  path = os.path.join(root, "resources/core.html")

  with open(path) as file:
    content = file.read().format(
      style = load.get("style", "default"),
      darkness = load.get("polarity", "light") == "dark",
      header = load.get("header", ""),
      content = content,
      source = "https://github.com/Sup2point0/Assort/" + file.path,
      version = __version__,
    )
  
  load["content"] = content
  load["path"] = "docs/" + load["path"] + ".html"

  return load


def extract_quarks(text: str) -> dict:
  '''Extract #QUARK quarks from Quarkdown-Flavoured Markdown.'''

  # TODO this is a bit inefficient, we should find a better way to do this
  if "#QUARK live!" not in text:
    raise Quarkless("#QUARK file inactive")

  root = os.path.split(os.path.abspath(__file__))[0]
  with open(os.path.join(root, "resources/tokens.json")) as file:
    tokens = json.load(file)["tokens"]

  with open(os.path.join(root, "resources/tokens-schema.json")) as file:
    defaults = json.load(file)["properties"]["tokens"]["items"]["defaultSnippets"][0]["body"]
  
  context: list[dict] = [defaults]
  flags = {}

  # TODO splitting twice is really, really slow, how do we optimise this
  for line in text.split("\n"):
    for part in line.split():
      for token in tokens:
        token = textualise.tokenise(token, defaults)

        try:
          check_open(context, part, token, flags)
        except ContextOpened:
          break
        except AssertionError:
          pass

        try:
          check_close(context, part, token)
        except AssertionError:
          pass

    while True:
      if context[-1]["ctx-persists"]:
        break
      if len(context) == 1:  # root context must always be active
        break
      
      close_ctx(context)

  return {**flags, "content": text}


def check_open(ctx: list[dict], part: str, token: dict, flags: dict):
  '''Check for contexts to open. Raises `AssertionError` if processing can be skipped, or `ContextOpened` if a context is successfully activated.'''

  can_activate(ctx, token)

  if ctx[-1]["kind"] == "html":
    assert "quark" in token["opens-ctx"]

  match = re.search(token["regex-open"], part)
  assert match is not None

  for flag, value in token["flags"].items():
    if isinstance(value, str):
      flags[flag] = part if value == "#VALUE" else value
    elif isinstance(value, dict):
      for key, val in value.items():
        if key == "add":
          flags[flag].append(part if val == "#VALUE" else value)

  if token["opens-ctx"]:
    ctx.append(token)
  else:
    for i in range(token["ctx-collapses"]):
      ctx.pop()

  raise ContextOpened()


def check_close(ctx: list[dict], part: str, token: dict):
  '''Check for contexts to close. Raises `AssertionError` if processing can be skipped.'''

  # context must be active to be deactivated
  assert ctx[-1]["opens-ctx"] == token["opens-ctx"]

  pattern = token["regex-close"]
  assert pattern is not None
  match = re.search(pattern, part)
  assert match is not None

  close_ctx(ctx)


def can_activate(ctx: list[dict], token: dict):
  '''Check if a context meets its activation requirements. Raises `AssertionError` if not.'''

  if token["required-ctx"]:
    assert ctx[-1]["opens-ctx"] == token["required-ctx"]

  if token["ctx-clashes"] is True or ctx[-1]["ctx-clashes"] is True:
    assert ctx[-1]["opens-ctx"] != token["opens-ctx"]
  elif token["ctx-clashes"] or ctx[-1]["ctx-clashes"]:
    assert ctx[-1]["opens-ctx"] not in token["ctx-clashes"]


def close_ctx(ctx):
  '''Close the current context, collapsing contexts if applicable.'''

  latest = ctx[-1]
  ctx.pop()
  for i in range(latest["ctx-collapses"]):
    ctx.pop()
