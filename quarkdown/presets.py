'''
Static resources.
'''

class url:
  google_fonts = "https://fonts.googleapis.com/css2?"
  styles = "https://raw.githack.com/Sup2point0/Quarkdown/main/quarkdown/resources/styles"

class css:
  def font(fonts: list[str]) -> str:
    '''Format the HTML `<link>` tag for loading fonts from Google Fonts.'''

    return f'''<link rel="stylesheet" type="text/css" href="{url.google_fonts}{"&".join(font for font in fonts)}&display=swap">'''
    
  def style(style: str) -> str:
    '''Format the HTML `<link>` tag for a given stylesheet.'''

    return f'''<link rel="stylesheet" type="text/css" href="{url.styles}/{style.lower()}">'''

dec_index = {
  "spring": 0.5,
  "summer": 4.5,
  "fall": 8.5,
  "autumn": 8.5,
  "winter": 12.5,
  **{str(i): i for i in range(13)},
  # 0 for unspecified months
}
