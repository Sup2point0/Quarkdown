'''
Implements the `ExportFile` class for representing files during quarkup.
'''

import datetime
import itertools
import json
import pathlib
from dataclasses import dataclass

from github.ContentFile import ContentFile

import suptools as sup
import config
from .. import presets
from .. import textualise


@ dataclass(kw_only = True)
class ExportFile:
  '''A container for all the export info of a file.'''

  file: ContentFile
  '''The original `github.ContentFile` fetched through the GitHub API. Only this parameter needs to be supplied when instantiating an `ExportFile`.'''

  source_path: str = None
  export_path: str = None
  export_path_frags: list[str] = None
  source_url: str = None

  title: str = "Assort"
  header: str = None
  content: str = None

  live: bool = None
  styles: list[str] = None
  duality: str = "light"
  indexes: list[str] = None
  shards: list[str] = None

  year: int = None
  season: str = None
  dec: int = None
  day: int = None
  date: datetime.date = None

  EXPORT_DATA = ["source_path", "export_path", "styles", "duality", "indexes", "shards"]

  def __post_init__(self):
    self.source_path = self.file.path
    self.source_url = self.file.html_url

  def __getitem__(self, key: str):
    return getattr(self, key)

  def set_flags(self, data: dict):
    '''Set file info from a given `dict`.

    All values are fully sanitised here. Should always be called before rendering the file.
    '''

    with open(config.ROOT / "quarkdown/resources/quarks.json") as source:
      flags = json.load(source)

    path = data.get("path", self.file.name) + ".html"
    self.export_path = textualise.sanitise_filename(path)
    self.export_path_frags = self.export_path.split("/")

    self.header = data.get("header", None)
    self.title = data.get("title", self.header or "Assort")

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
    )).lower()

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
      self.date = datetime.date(
        year = int(flags["year"]),
        month = presets.dec_index.get(flags.get("dec", 0), 0),
        day = flags.get("day", 1),
      )

  def export_dict(self) -> dict:
    '''Extract a concise `dict` representation of the exported file.'''

    attrs = vars(self)
    return {each: attrs[each] for each in attrs if each in self.EXPORT_DATA}
