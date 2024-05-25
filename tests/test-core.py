'''
Test export metadata handling.
'''

# we really need to find a proper way to do this
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])

import quarkdown as qk


def test_single(file):
  file.content = '''
    <!-- #QUARK live!
      EXPORT: testing/test
      STYLE: default
      DUALITY: light
      INDEX: tests
      DATE: 24
    -->
  '''

  result = qk.extract(file)

  assert result.live is True
  assert result.path == "testing/test"
  assert result.style == ["default"]
  assert result.duality == "light"
  assert result.index == ["tests"]
  assert result.date == ["24"]


def test_multi():
  file = '''
  <!-- #QUARK live!
    EXPORT: testing/tester/test scarlet/herring
    STYLE: default special testing
    DUALITY: light ignore
    INDEX: tests testing
    DATE: 24 04 02
  -->
'''

  result = qk.extract(file)

  assert result.live is True
  assert result.path == "testing/tester/test"
  assert result.style == ["default", "special", "testing"]
  assert result.duality == "light"
  assert result.index == ["tests", "testing"]
  assert result.date == ["24", "04", "02"]
