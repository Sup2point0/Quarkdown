'''
Implements the `RepoOptions` class for configuring repo quarkup options.
'''

from dataclasses import dataclass


@ dataclass(kw_only = True)
class RepoConfig:
  '''A container for configuring how a repo is exported.'''

  export_directory: str = "docs"
