class Context:
  '''Represents a parsing context for dynamic awareness of the text being processed.'''

  def __init__(self, ctx: dict):
    '''Convert a `dict` into a `Context` object.'''

    self.shard = ctx["opens-ctx"]
    # self.~ = self.shard[:self.shard.index(".")]
    self.kind = ctx["kind"]

    self.clashes = ctx.get("ctx-clashes", [])
    self.persists = ctx.get("ctx-persists", False)

    self.autocloses = (ctx.get("regex.close") == "#AUTO")
    self.collapses = ctx.get("ctx-collapses", 0)

  def done(self) -> bool:
    '''Check if context should be deactivated (when deactivation requisites are met).'''

    if self.kind == "#FLAG":
      return True

    # if self.autocloses or not self.persists:
    #   return True
