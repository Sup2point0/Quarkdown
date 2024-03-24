'''
Implements the Quarkdown parsing engine.
'''

import json
import re
import os

from io import StringIO

from . import textualise


__all__ = ["export"]


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK LIVE` flag.'''
  pass

class ContextOpened(Exception):
  '''Exception raised when a context has been successfully activated.'''
  pass



def export(text: str) -> dict:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  load = extract_quarks(text)

  content = load["content"]
  content = textualise.render_html(content)
  content = textualise.clear_comments(content)

  root = os.path.split(os.path.abspath(__file__))[0]
  with open(os.path.join(root, "resources/core.html")) as file:
    content = file.read().format(
      header = load["flags"].get("header", ""),
      content = load["content"],
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

  # TODO splitting is really slow, how do we optimise this
  for part in re.split(" ", text):
    for token in tokens:
      token = textualise.tokenise(token, defaults)

      try:
        check_open(context, part, token, flags)
      except ContextOpened:
        break
      except AssertionError:
        continue

      try:
        check_close(context, part, token, flags)
      except AssertionError:
        continue

  return {"content": text, **flags}


def check_open(ctx: list[dict], part: str, token: dict, flags: dict):
  '''Check for contexts to open. Raises `AssertionError` if processing can be skipped, or `ContextOpened` if a context is successfully activated.'''

  assert not should_skip(ctx, token)

  if ctx[-1]["kind"] == "html":
    assert "quark" in token["shard"]

  match = re.search(token["regex-open"], part)
  assert match is not None

  can_activate(ctx, token)

  for flag, value in token["flags"].items():
    flags[flag] = part if value == "#VALUE" else value

  if token["opens-ctx"]:
    ctx.append(token)
  else:
    for i in range(token["ctx-collapses"]):
      ctx.pop()

  raise ContextOpened()


def check_close(ctx: list[dict], part: str, token: dict, flags: dict):
  '''Check for contexts to close. Raises `AssertionError` if processing can be skipped.'''

  # context must be active to be deactivated
  assert ctx[-1].shard == token["opens-ctx"]

  pattern = token["regex-close"]
  assert pattern is not None
  match = re.search(pattern, part)
  assert match is not None

  cx = ctx[-1]
  ctx.pop()
  for i in range(cx["ctx-collapses"]):
    ctx.pop()


def should_skip(ctx: list[dict], token: dict) -> bool:
  '''Check if processing for a token should be skipped (when activation requisites are not fulfilled).'''

  if token["required-ctx"]:
    if ctx[-1]["shard"] != token["required-ctx"]:
      return True

  if token["ctx-clashes"] is True:
    if ctx[-1]["shard"] == token["opens-ctx"]:
      return True
  elif token["ctx-clashes"]:
    if ctx[-1]["shard"] in token["ctx-clashes"]:
      return True


def can_activate(ctx: list[dict], token: dict):
  '''Check if a context meets its activation requirements.'''
 
  if token["required-ctx"]:
    assert ctx[-1]["shard"] == token["required-ctx"], "required ctx not active"

  if (
       ctx[-1]["ctx-clashes"] is True
    or token["ctx-clashes"] is True
    or isinstance(ctx[-1]["ctx-clashes"], str)
    or isinstance(token["ctx-clashes"], str)
  ):
    assert token["opens-ctx"] not in ctx, "clashing with active ctx"
 
  # FIXME
  # if isinstance(ctx[-1].clashes, list):
  #   assert token["opens-ctx"] not in ctx[-1].clashes
  # if isinstance(token["ctx-clashes"], list):
  #   assert ctx[-1].shard not in token["opens-ctx"]
