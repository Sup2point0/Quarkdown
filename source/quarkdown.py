'''
Quarkdown
v1.0.0

A Markdown to HTML renderer
by Sup#2.0 (@Sup2point0)

Available at: <https://github.com/Sup2point0/Quarkdown>
'''

import json
import re

from io import StringIO

import requests

from context import Context


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK LIVE` flag.'''

  pass


def process_quarks(text: str) -> dict:
  '''Extract #QUARK quarks from Quarkdown-Flavoured Markdown.'''

  # TODO this is a bit inefficient, we should find a better way to do this
  if "#QUARK LIVE" not in text:
    raise Quarkless("#QUARK file inactive")

  with open("resources/tokens.json") as file:
    tokens = json.load(file)["quarks"]

  content = StringIO()
  flags = {}
  context = [Context({"kind": "#ROOT", "opens-ctx": None})]
  ctx = lambda: context[-1]

  # TODO splitting is really slow, how do we optimise this
  for part in re.split(" ", text):
    for token in tokens:
        if _should_skip_(context, token):
          continue

        if context[-1].kind == "html":
          if "quark" not in token["id"]:
            continue

        # parse by word
        # check which token matches regex-open
        # activate ctx
        # trigger flags
        # check which token matches regex-close

        # using try-except to reduce any more excessive indentation than there already is!
        try:
          match = re.search(token["regex.open"], part)
          assert match is not None

          assert _can_activate(ctx(), token)

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

          for flag, value in token["flags"].items():
            flags[flag] = part if value == "#VALUE" else value

          if token["opens-ctx"] is not None:
            context.append(Context(token))

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

    # collapse context stack
    while (cx := ctx()).done():
      context.pop()
      for i in range(cx.collapses):
        context.pop()

  return {
    "content": text,#content,
    "flags": flags,
  }


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


def export(data: dict) -> dict:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  with open("resources/core.html") as file:
    data["content"] = file.read().format(
      header = data["flags"]["header"],
      content = data["content"],
    )
  
  return data


def _should_skip_(ctx, token) -> bool:
  '''Check if processing for a token should be skipped (when activation requisites are not fulfilled).'''

  if ctx is None:
    return False

  if token["required-ctx"]:
    if ctx[-1].shard != token["required-ctx"]:
      return True

  if token["ctx-clashes"]:
    if ctx[-1].shard in token["ctx-clashes"]:
      return True


def _can_activate(ctx: list[Context], token: dict) -> True:
  '''Check if a context meets its activation requirements.'''
 
  assert ctx[-1].shard == token["requires-ctx"]
 
  if (
       ctx[-1].clashes is True
    or token["ctx-clashes"] is True
    or isinstance(ctx[-1].clashes, str)
    or isinstance(token["ctx-clashes"], str)
  ):
    assert token["opens-ctx"] not in ctx
 
  # FIXME
  if isinstance(ctx.clashes, list):
    assert token["opens-ctx"] not in ctx.clashes
  if isinstance(token["ctx-clashes"], list):
    assert ctx.shard not in token["opens-ctx"]
