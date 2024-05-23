'''
Static resources.
'''

from typing import Iterable


class defaults:
  fonts = ("abel", "montserrat")


class url:
  styles = "https://raw.githack.com/Sup2point0/Quarkdown/main/quarkdown/resources/styles"
  GoogleFonts = "https://fonts.googleapis.com/css2?"
  MathJax = "<script type="text/javascript" src="https://d3eoax9i5htok0.cloudfront.net/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"> </script>"

  fonts = {
    "abel": "Abel",
    "geologica": "Geologica:slnt,wght@-12..0,100..900",
    "montserrat": "Montserrat:ital,wght@0,100..900;1,100..900",
    "nanum": "Nanum+Pen+Script",
    "outfit": "Outfit:wght@100..900",
    "readex": "Readex+Pro:wght@160..700",
    "sen": "Sen:wght@400..800",
    "shadows into light two": "Shadows+Into+Light+Two",
  }
  '''Google Fonts URLs.'''


class css:
  def fonts(fonts: Iterable[str]) -> str:
    '''Format the HTML `<link>` tag for loading fonts from Google Fonts.'''

    return (
      f'''<link rel="stylesheet" type="text/css" href="'''
      f'''{url.GoogleFonts}{"&".join("family=" + url.fonts[font.lower] for font in fonts)}&display=swap">'''
    )
    
  def style(style: str) -> str:
    '''Format the HTML `<link>` tag for a given stylesheet.'''

    style = style.lower()
    if style == "auto":
      style = "default"

    return f'''<link rel="stylesheet" type="text/css" href="{url.styles}/{style}">'''


dec_index = {
  "spring": 0.5,
  "summer": 4.5,
  "fall": 8.5,
  "autumn": 8.5,
  "winter": 12.5,
  **{str(i): i for i in range(13)},
  # 0 for unspecified months
}
