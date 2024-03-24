'''
Implements utility classes for use in the parsing engine.
'''


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK LIVE` flag.'''

  pass


class ContextOpened(Exception):
  '''Exception raised when a context has been successfully activated.'''
  pass


# class Context:
#   '''Represents a parsing context for dynamic awareness of the text being processed.'''

#   def __init__(self, ctx: dict):
#     '''Convert a `dict` into a `Context` object.'''

#     self.shard = ctx["opens-ctx"]
#     # self.~ = self.shard[:self.shard.index(".")]
#     self.kind = ctx["kind"]

#     self.clashes = ctx.get("ctx-clashes", [])
#     self.persists = ctx.get("ctx-persists", False)

#     self.autocloses = (ctx.get("regex.close") == "#AUTO")
#     self.collapses = ctx.get("ctx-collapses", 0)

#   def done(self) -> bool:
#     '''Check if context should be deactivated (when deactivation requisites are met).'''

#     # if self.autocloses or not self.persists:
#     #   return True
