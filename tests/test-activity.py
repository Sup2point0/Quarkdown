'''
Test `live!` and `dead!` quarks.
'''

import pytest

import quarkdown as qk


def test_live_positive(file):
  file.content = '''
    <!-- #QUARK live! -->
  '''

  result = qk.extract(file)

  assert result.live is True, "flag [live] not triggered!"


def test_live_negative(file):
  file.content = '''
    <!-- #QUARK -->
  '''

  with pytest.raises(qk.Quarkless):
    qk.extract(file)


def test_dead_positive(file):
  file.content = '''
    <!-- #QUARK dead! -->
    <!-- #QUARK live! -->
  '''

  with pytest.raises(qk.Quarkless):
    result = qk.extract(file)

  assert result.live is False
