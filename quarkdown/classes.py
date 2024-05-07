'''
Utility classes.
'''

import datetime
import itertools
import json
import pathlib
from dataclasses import dataclass

from github.ContentFile import ContentFile

import suptools as sup
from . import presets


class Quarkless(Exception):
  '''Exception raised when a file has no `#QUARK LIVE` flag.'''
  pass

class ContextOpened(Exception):
  '''Exception raised when a context has been successfully activated.'''
  pass


@ dataclass(kw_only = True, slots = True)
class ExportFile:
  '''A container for all the export info of a file.'''

  file: ContentFile

  orig_path: str = None
  export_path: str = None
  source_url: str = None

  title: str = None
  header: str = None
  content: str = None

  styles: list[str] = None
  duality: str = "light"
  indexes: list[str] = None
  shard: list[str] = None

  year: int = None
  season: str = None
  dec: int = None
  day: int = None
  date: datetime.date = None

  def set_flags(self, data: dict):
    '''Set file info from a given `dict`.

    All values are fully sanitised here.
    '''

    path = pathlib.Path(__file__).absolute.parent
    path = path.join("resources", "quarks.json")

    with open(path) as file:
      flags = json.load(file)

    path = data.get("path", self.file.name)
    self.export_path = textualise.sanitise_filename(path)
    self.export_path_frags = self.export_path.split("\n")

    self.header = data.get("header", None)

    styles = data.get("styles", ["auto"])
    self.styles = [
      "default" if style.lower() == "auto" else style.lower()
      for style in sup.it.unique(styles)
    ]

    # if no duality set, find default by cascading backwards
    duality = (
      flags["styles"][style].get("duality", None)
      for style in reversed(self.styles)
    )
    self.duality = data.get("duality", next(
      (each for each in duality if each),
      flags["styles"]["default"]["duality"]
    ))

    # indexes listed by relevance so order retained
    indexes = data.get("indexes", [])
    self.indices = list(sup.it.unique(
      itertools.chain.from_iterable(
        self.export_path_frags if index.lower() == "auto" else index.lower()
        for index in indexes
      )
    ))

    # shards sorted alphabetically so intermediate order irrelevant
    shards = data.get("shards", [])
    self.shards = sorted(list(set(
      itertools.chain.from_iterable(
        self.indexes if shard.lower() == "auto" else shard.lower()
        for shard in shards
      )
    )))

    if flags.get("year", None) is not None:
      self.date = date(
        year = int(flags["year"]),
        month = presets.dec_index.get(flags.get("dec", 0), 0),
        day = flags.get("day", 1),
      )
