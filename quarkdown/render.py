'''
Assembles all the individual parts of a page to construct the final HTML file.
'''

import base64

import config
from . import presets
from . import textualise
from . import quarkify
from .classes import ExportFile, RepoConfig


__all__ = ["render"]


def render(file: ExportFile, repo_config: RepoConfig) -> ExportFile:
  '''Render Quarkdown-Flavoured Markdown to HTML, extracting content and metadata.'''

  text = base64.b64decode(file.content).decode()
  load = quarkify.extract(text)

  # isn't this pipeline nice... maybe there's a way to do this more succinctly?
  content = load.content
  content = textualise.render_html(content)
  content = textualise.clear_comments(content)
  content = textualise.indent(content, 6)

  header = load.header
  header = textualise.indent(header, 6)

  fonts = presets.css.fonts(repo_config.get("fonts", presets.defaults.fonts))
  styles = "  \n".join(presets.css.style(style) for style in load.get("style", ["default"]))

  with open(config.ROOT / "quarkdown/resources/parts/core.html") as source:
    content = source.read().format(
      title = load.get("title", "Assort"),
      fonts = fonts,
      styles = styles,
      dark = load.get("duality", "light").lower(),
      header = header,
      content = content,
      source = "https://github.com/Sup2point0/Assort/" + file.path,
      version = config.__version__,
    )
  
  load["content"] = content
  load["path"] = "docs/" + load["path"] + ".html"

  return load
