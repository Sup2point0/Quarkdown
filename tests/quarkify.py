# we really need to find a proper way to do this
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])

from quarkdown import quarkify


def test_live_positive():
  result = quarkify.extract_quarks('''
    test
    <!-- #QUARK live! -->
    <!-- #QUARK
    EXPORT: testing/test
    -->
    test
  ''')

  assert result["live"] is True, "live flag not triggered!"
  assert result["path"] == "testing/test", "export path incorrect!"


def test_live_negative():
  skips = False
  
  try:
    quarkify.extract_quarks('''
      test
      test
      <!-- #QUARK -->
      test
      test
    ''')
  except quarkify.Quarkless:
    skips = True

  assert skips


def test_dead():
  skips = False

  try:
    quarkify.extract_quarks('''
      test
      test
      <!-- #QUARK dead! -->
      <!-- #QUARK live! -->
      test
      test
    ''')
  except quarkify.Quarkless:
    skips = True

  assert skips


def test_data_single():
  result = quarkify.extract_quarks('''
    <!-- #QUARK live! -->
    <!-- #QUARK
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
