'''
Assembles all the individual parts of a page to construct the final HTML file.
'''

import pathlib

import config
from . import presets
from . import textualise
from . import quarkify
from .classes import ExportFile, RepoConfig


__all__ = ["construct"]


def construct(file: ExportFile, repo_config: RepoConfig) -> ExportFile:
  '''Render Quarkdown-Flavoured Markdown to HTML.'''

  # isn't this pipeline nice... maybe there's a way to do this more succinctly?
  content = file.content
  content = textualise.render_html(content)
  content = textualise.clear_comments(content)
  content = textualise.indent(content, 6)

  with open(config.ROOT / "quarkdown/resources/parts/core.html") as source:
    content = source.read().format(
      title = file.title,
      fonts = presets.css.fonts(repo_config.get("fonts", presets.defaults.fonts)),
      styles = "  \n".join(presets.css.style(style) for style in file.styles),
      dark = file.duality,
      header = render_header(file),
      content = content,
      source = file.source_url,
      version = config.__version__,
    )
  
  file.path = str(pathlib.Path(repo_config.export_directory) / file.path)

  return file


def render_header(file: ExportFile) -> str:
  '''Render the header of a page, if it exists.'''

  if file.header is None:
    return ""
  
  with open(config.ROOT / "quarkdown/resources/parts/header.html") as source:
    return source.read().format(text = file.header)
