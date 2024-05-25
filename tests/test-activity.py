'''
Test `live!` and `dead!` quarks.
'''

import pytest

import quarkdown as qk


def test_live_positive(source, encode):
  file = qk.ExportFile(file = source)
  file.content = encode('''
    <!-- #QUARK live! -->
  ''')

  result = qk.extract(file)

  assert result.live is True, "flag [live] not triggered!"


def test_live_negative(source, encode):
  file = qk.ExportFile(file = source)
  file.content = encode('''
    <!-- #QUARK -->
  ''')

  with pytest.raises(qk.Quarkless):
    qk.extract(file)


def test_dead_positive(source, encode):
  file = qk.ExportFile(file = source)
  file.content = encode('''
    <!-- #QUARK dead! -->
    <!-- #QUARK live! -->
  ''')

  result = None

  with pytest.raises(qk.Quarkless):
    result = qk.extract(file)
