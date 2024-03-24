'''
Implements the Quarkdown parsing engine.
'''

import json
import re
import os

from io import StringIO

from .structs import Quarkless, ContextOpened
from .textualise import tokenise


def export(data: dict) -> dict:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  with open(".resources/core.html") as file:
    data["content"] = file.read().format(
      header = data["flags"]["header"],
      content = data["content"],
    )
  
  return data


def process_quarks(text: str) -> dict:
  '''Extract #QUARK quarks from Quarkdown-Flavoured Markdown.'''

  # TODO this is a bit inefficient, we should find a better way to do this
  if "#QUARK LIVE" not in text:
    raise Quarkless("#QUARK file inactive")

  # FIXME path
  with open("../quarkdown/resources/tokens.json") as file:
    tokens = json.load(file)["tokens"]

  defaults = tokens["tokens"]["items"]["defaultSnippets"]
  context = [tokenise({}, defaults)]
  flags = {}

  # TODO splitting is really slow, how do we optimise this
  for part in re.split(" ", text):
    print(f"\nprocessing {part}")
    print(f"context = {', '.join('None' if each.shard is None else each.shard for each in context)}")
    for token in tokens:
      token = tokenise(token, defaults)
      print(f"checking {token['shard']}")

      '''
      parse by word
      check which token matches regex-open
      activate ctx
      trigger flags
      check which token matches regex-close
      '''

      try:
        _check_open(context, part, token, flags)
      except ContextOpened:
        break
      except AssertionError:
        continue

      try:
        _check_close(context, part, token, flags)
      except AssertionError:
        continue
    
    print(f"flags = {flags}")

  return {
    "content": text,#content,
    "flags": flags,
  }


def _check_open(ctx: list[dict], part: str, token: dict, *, flags: dict):
  '''Check for contexts to open. Raises `AssertionError` if processing can be skipped, or `ContextOpened` if a context is successfully activated.'''

  print(f"checking {token['shard']}")
  assert not _should_skip_(ctx[-1], token)

  if ctx[-1]["kind"] == "html":
    assert "quark" in token["shard"]

  match = re.search(token["regex-open"], part)
  assert match is not None

  _can_activate(ctx, token)

  for flag, value in token["flags"].items():
    flags[flag] = part if value == "#VALUE" else value

  if token["opens-ctx"]:
    ctx.append(token)
  else:
    for i in range(token["ctx-collapses"]):
      ctx.pop()

  raise ContextOpened()


def _check_close(ctx: list[dict], part: str, token: dict, *, flags: dict):
  '''Check for contexts to close. Raises `AssertionError` if processing can be skipped.'''

  print(f"current = {ctx().shard}, target = {token.get('opens-ctx', None)}")
  # context must be active to be deactivated
  assert ctx[-1].shard == token["opens-ctx"]

  pattern = token["regex-close"]
  assert pattern is not None
  match = re.search(pattern, part)
  print(f"closing match = {match}")
  assert match is not None

  cx = ctx[-1]
  ctx.pop()
  for i in range(cx["ctx-collapses"]):
    ctx.pop()


def _should_skip_(ctx, token) -> bool:
  '''Check if processing for a token should be skipped (when activation requisites are not fulfilled).'''

  if token["required-ctx"]:
    if ctx.shard != token["required-ctx"]:
      return True

  if token["ctx-clashes"] is True:
    if ctx.shard == token["opens-ctx"]:
      return True
  elif token["ctx-clashes"]:
    if ctx.shard in token["ctx-clashes"]:
      return True


def _can_activate(ctx: list[dict], token: dict):
  '''Check if a context meets its activation requirements.'''
 
  if token["required-ctx"]:
    assert ctx[-1].shard == token["required-ctx"], "required ctx not active"

  if (
       ctx[-1].clashes is True
    or token["ctx-clashes"] is True
    or isinstance(ctx[-1].clashes, str)
    or isinstance(token["ctx-clashes"], str)
  ):
    assert token["opens-ctx"] not in ctx, "clashing with active ctx"
 
  # FIXME
  # if isinstance(ctx[-1].clashes, list):
  #   assert token["opens-ctx"] not in ctx[-1].clashes
  # if isinstance(token["ctx-clashes"], list):
  #   assert ctx[-1].shard not in token["opens-ctx"]
