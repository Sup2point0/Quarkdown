# we really need to find a proper way to do this
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])

from quarkdown import quarkify


def test_positive():
  result = quarkify.extract_quarks('''
    <!-- #QUARK live! -->
    <!-- #QUARK
    EXPORT: testing/test
    -->
  ''')

  assert result["live"] is True, "live flag not triggered!"
  assert result["path"] == "testing/test", "export path incorrect!"


def test_negative():
  skips = False
  
  try:
    quarkify.extract_quarks('''
      testing
      <!-- #QUARK -->
    ''')
  except quarkify.Quarkless:
    skips = True

  assert skips