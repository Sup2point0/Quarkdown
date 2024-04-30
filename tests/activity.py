'''
Test `live!` and `dead!` quarks.
'''

# we really need to find a proper way to do this
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])

from quarkdown import quarkify


def test_live_positive():
  result = quarkify.extract_quarks('''
    <!-- #QUARK live! -->
  ''')

  assert "live" in result, "flag [live] doesn’t exist!"
  assert result["live"] is True, "flag [live] not triggered!"


def test_live_negative():
  skips = False
  
  try:
    quarkify.extract_quarks('''
      <!-- #QUARK -->
    ''')
  except quarkify.Quarkless:
    skips = True

  assert skips, "exception [Quarkless] not raised!"


def test_dead_positive():
  skips = False

  try:
    result = quarkify.extract_quarks('''
      <!-- #QUARK dead! -->
      <!-- #QUARK live! -->
    ''')
  except quarkify.Quarkless:
    skips = True
    result = None

  if result:
    assert result.get("live", False) is not True, "flag [live] set to True instead of False!"
  assert skips, "exception [Quarkless] not raised!"
