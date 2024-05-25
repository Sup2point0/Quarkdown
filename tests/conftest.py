import base64
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

  def set_flags(self, *args, **kwargs):
    return self


@ pytest.fixture(scope = "module")
def source():
  return Placeholder()


@ pytest.fixture(scope ="module")
def encode():
  def apply(content: str) -> str:
    return base64.b64encode(content.encode())
  
  return apply
