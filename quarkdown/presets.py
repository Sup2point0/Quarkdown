'''
Static resources.
'''


class defaults:
  fonts = ["abel", "montserrat"]


class url:
  google_fonts = "https://fonts.googleapis.com/css2?"
  styles = "https://raw.githack.com/Sup2point0/Quarkdown/main/quarkdown/resources/styles"

  fonts = {
    "abel": "family=Abel",
    "geologica": "Geologica:slnt,wght@-12..0,100..900",
    "montserrat": "family=Montserrat:ital,wght@0,100..900;1,100..900",
    "nanum": "family=Nanum+Pen+Script",
    "outfit": "family=Outfit:wght@100..900",
    "sen": "family=Sen:wght@400..800",
    "shadows into light two": "family=Shadows+Into+Light+Two",
  }
  '''Google Fonts URLs.'''


class css:
  def fonts(fonts: list[str]) -> str:
    '''Format the HTML `<link>` tag for loading fonts from Google Fonts.'''

    return (
      f'''<link rel="stylesheet" type="text/css" href="'''
      f'''{url.google_fonts}{"&".join(url.fonts[font.lower] for font in fonts)}&display=swap">'''
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
