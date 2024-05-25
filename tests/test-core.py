'''
Test export metadata handling.
'''

import datetime

import quarkdown as qk


def test_single(source, encode):
  file = qk.ExportFile(file = source)
  file.content = encode('''
    <!-- #QUARK live!
      EXPORT: testing/test
      STYLE: default
      DUALITY: light
      INDEX: tests
      DATE: 24
    -->
  ''')

  result = qk.extract(file)

  assert result.live is True
  assert result.export_path == "testing/test.html"
  assert result.styles == ["default"]
  assert result.duality == "light"
  assert result.indexes == ["tests"]
  assert result.date == datetime.date(24, 0, 1)


def test_multi(source, encode):
  file = qk.ExportFile(file = source)
  file.content = encode('''
  <!-- #QUARK live!
    EXPORT: testing/tester/test scarlet/herring
    STYLE: default special testing
    DUALITY: light ignore
    INDEX: tests testing
    DATE: 24 04 02
  -->
  ''')

  result = qk.extract(file)

  assert result.live is True
  assert result.export_path == "testing/tester/test.html"
  assert result.styles == ["default", "special", "testing"]
  assert result.duality == "light"
  assert result.indexes == ["tests", "testing"]
  assert result.date == datetime.date("24", "04", "02")
