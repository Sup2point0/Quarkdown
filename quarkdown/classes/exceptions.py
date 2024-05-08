'''
Implements exceptions used internally in Quarkdown.
'''


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK live!` flag.'''
  
  pass


class IsIndex(Exception):
  '''Exception raised when a file has a `#QUARK index!` flag.'''
  
  pass


class ContextOpened(Exception):
  '''Exception raised when a context has been successfully activated.'''
  
  pass
