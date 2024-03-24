'''
Implements the Quarkdown parsing engine.
'''

import json
import re

from io import StringIO

from .structs import Context, Quarkless


def export(data: dict) -> dict:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  with open("resources/core.html") as file:
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

  with open("resources/tokens.json") as file:
    tokens = json.load(file)["tokens"]

  content = StringIO()
  flags = {}
  context = [Context({"kind": "#ROOT", "opens-ctx": None})]
  ctx = lambda: context[-1]

  # TODO splitting is really slow, how do we optimise this
  for part in re.split(" ", text):
    print(f"\nprocessing {part}")
    print(f"context = {', '.join('None' if each.shard is None else each.shard for each in context)}")
    for token in tokens:
      print(f"checking {token['shard']}")
      for i in range(1):
        if _should_skip_(ctx(), token):
          continue

        if ctx().kind == "html":
          if "quark" not in token["shard"]:
            continue

        '''
        parse by word
        check which token matches regex-open
        activate ctx
        trigger flags
        check which token matches regex-close
        '''

        # using try-except to reduce any more excessive indentation than there already is!
        try:
          match = re.search(token["regex-open"], part)
          assert match is not None

          _can_activate(context, token)

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

          for flag, value in token.get("flags", {}).items():
            flags[flag] = part if value == "#VALUE" else value

          if token.get("opens-ctx", None):
            context.append(Context(token))
          else:
            for i in range(token.get("ctx-collapses", 0)):
              context.pop()

          print("breaking")
          break

        except AssertionError:
          pass

      # close context
      try:
        print(f"current = {ctx().shard}, target = {token.get('opens-ctx', None)}")
        assert ctx().shard == token.get("opens-ctx", None)

        pattern = token.get("regex-close", None)
        assert pattern is not None
        match = re.search(pattern, part)
        print(f"closing match = {match}")
        assert match is not None

        cx = ctx()
        context.pop()
        for i in range(cx.collapses):
          context.pop()

        # suf = info["html.close"]
        # if suf is None:
        #   suf = "</div>"
        # content.write(f"{string}{suf}")

      except AssertionError:
        pass

    # collapse context stack
    while (cx := ctx()).done():
      context.pop()
    
    print(f"flags = {flags}")

  return {
    "content": text,#content,
    "flags": flags,
  }


def _should_skip_(ctx, token) -> bool:
  '''Check if processing for a token should be skipped (when activation requisites are not fulfilled).'''

  if token.get("required-ctx", None):
    if ctx.shard != token["required-ctx"]:
      return True

  if token.get("ctx-clashes", None) is True:
    if ctx.shard == token["opens-ctx"]:
      return True
  elif token.get("ctx-clashes", None):
    if ctx.shard in token["ctx-clashes"]:
      return True


def _can_activate(ctx: list[Context], token: dict):
  '''Check if a context meets its activation requirements.'''
 
  if token.get("required-ctx", None):
    assert ctx[-1].shard == token["required-ctx"], "required ctx not active"

  if (
       ctx[-1].clashes is True
    or token.get("ctx-clashes", None) is True
    or isinstance(ctx[-1].clashes, str)
    or isinstance(token.get("ctx-clashes", None), str)
  ):
    assert token.get("opens-ctx", None) not in ctx, "clashing with active ctx"
 
  # FIXME
  # if isinstance(ctx[-1].clashes, list):
  #   assert token["opens-ctx"] not in ctx[-1].clashes
  # if isinstance(token["ctx-clashes"], list):
  #   assert ctx[-1].shard not in token["opens-ctx"]
