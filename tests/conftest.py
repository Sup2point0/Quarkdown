import pytest

import suptools as sup


class Placeholder:
  def __init__(self):
    sup.Object.__init__(self,
      name = "testing",
      path = "testing",
      html_url = "https://github.com/Sup2point0",
      content = None,
    )

  def set_flags(self):
    return self


@ pytest.fixture(scope = "module")
def file():
  return Placeholder()
