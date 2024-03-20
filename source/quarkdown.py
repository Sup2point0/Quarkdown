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

import render


def textualise(source) -> namedtuple:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  with open("tokens.json") as file:
    tokens = json.load(file)

  content = StringIO()
  context = []

  for line in source:
    for token in tokens["line"]:
      ...
    
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

    content.write("\n")

  path = "test"
  Export = namedtuple("Export", ["path", "content"])

  return Export(path, content.getvalue())


def _should_skip_(ctx, token) -> bool:
  '''Check if processing for a token should be skipped (when activation requisites are not fulfilled).'''

  if token["required-ctx"]:
    if ctx[-1].shard != token["required-ctx"]:
      return True

  if token["ctx-clashes"]:
    if ctx[-1].shard in token["ctx-clashes"]:
      return True
