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


def test_data_single():
  result = quarkify.extract_quarks('''
    <!-- #QUARK live!
    EXPORT: testing/test
    STYLE: default
    DUALITY: light
    INDEX: tests
    DATE: 24
    -->
  ''')

  assert result["live"] is True
  assert result["path"] == "testing/test"
  assert result["style"] == ["default"]
  assert result["duality"] == "light"
  assert result["index"] == ["tests"]
  assert result["date"] == ["24"]


def test_data_multi():
  result = quarkify.extract_quarks('''
    <!-- #QUARK live!
    EXPORT: testing/tester/test scarlet/herring
    STYLE: default special testing
    DUALITY: light ignore
    INDEX: tests testing
    DATE: 24 04 02
    -->
  ''')

  assert result["live"] is True
  assert result["path"] == "testing/tester/test"
  assert result["style"] == ["default", "special", "testing"]
  assert result["duality"] == "light"
  assert result["index"] == ["tests", "testing"]
  assert result["date"] == ["24", "04", "02"]
