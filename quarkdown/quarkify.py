'''
Implements the Quarkdown parsing engine.
'''

import json
import re
import os

from . import textualise


__all__ = ["export"]
__version__ = "1.1.0"


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK LIVE` flag.'''
  pass

class ContextOpened(Exception):
  '''Exception raised when a context has been successfully activated.'''
  pass


def export(text: str) -> dict:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  load = extract_quarks(text)
  print(f"load = {load}")

  content = load["content"]
  content = textualise.render_html(content)
  content = textualise.clear_comments(content)

  root = os.path.split(os.path.abspath(__file__))[0]
  path = os.path.join(root, "resources/core.html")
  with open(path) as file:
    content = file.read().format(
      darkness = load.get("polarity", "#LIGHT") == "#DARK",
      header = load.get("header", ""),
      content = content,
      source = "https://github.com/Sup2point0/Assort/" + load.get("source", ""),
      version = __version__,
    )
  
  load["content"] = content
  load["path"] = "docs/" + load["path"] + ".html"
  return load


def extract_quarks(text: str) -> dict:
  '''Extract #QUARK quarks from Quarkdown-Flavoured Markdown.'''

  # TODO this is a bit inefficient, we should find a better way to do this
  if "#QUARK LIVE" not in text:
    raise Quarkless("#QUARK file inactive")

  # FIXME path
  root = os.path.split(os.path.abspath(__file__))[0]
  with open(os.path.join(root, "resources/tokens.json")) as file:
    tokens = json.load(file)["tokens"]

  with open(os.path.join(root, "resources/tokens-schema.json")) as file:
    defaults = json.load(file)["properties"]["tokens"]["items"]["defaultSnippets"][0]["body"]
  
  context = [textualise.tokenise({}, defaults)]
  flags = {}

  # TODO splitting is pretty slow, how do we optimise this
  for part in text.split():
    print(f"processing '{part}', context = [" + ", ".join(each["shard"] for each in context) + "]")  # NOTE testing
    for token in tokens:
      token = textualise.tokenise(token, defaults)

      try:
        check_open(context, part, token, flags)
      except ContextOpened:
        break
      except AssertionError:
        pass

      try:
        check_close(context, part, token, flags)
      except AssertionError:
        pass
        
    # print(f"finished '{part}', context = [" + ", ".join(each["shard"] for each in context) + "]")  # NOTE testing

  return {**flags, "content": text}


def check_open(ctx: list[dict], part: str, token: dict, flags: dict):
  '''Check for contexts to open. Raises `AssertionError` if processing can be skipped, or `ContextOpened` if a context is successfully activated.'''

  can_activate(ctx, token)

  if ctx[-1]["kind"] == "html":
    assert "quark" in token["opens-ctx"]

  match = re.search(token["regex-open"], part)
  assert match is not None

  for flag, value in token["flags"].items():
    flags[flag] = part if value == "#VALUE" else value
  print(f"flags = {flags}")

  if token["opens-ctx"]:
    ctx.append(token)
  else:
    for i in range(token["ctx-collapses"]):
      ctx.pop()

  print(f"ACTIVATED {token['shard']}")
  raise ContextOpened()


def check_close(ctx: list[dict], part: str, token: dict, flags: dict):
  '''Check for contexts to close. Raises `AssertionError` if processing can be skipped.'''

  # context must be active to be deactivated
  assert ctx[-1]["opens-ctx"] == token["opens-ctx"]

  pattern = token["regex-close"]
  assert pattern is not None
  match = re.search(pattern, part)
  assert match is not None

  cx = ctx[-1]
  ctx.pop()
  for i in range(cx["ctx-collapses"]):
    ctx.pop()


def can_activate(ctx: list[dict], token: dict):
  '''Check if a context meets its activation requirements. Raises `AssertionError` if not.'''

  if token["required-ctx"]:
    assert ctx[-1]["opens-ctx"] == token["required-ctx"]

  if token["ctx-clashes"] is True or ctx[-1]["ctx-clashes"] is True:
    assert ctx[-1]["opens-ctx"] != token["opens-ctx"]
  elif token["ctx-clashes"] or ctx[-1]["ctx-clashes"]:
    assert ctx[-1]["opens-ctx"] not in token["ctx-clashes"]
