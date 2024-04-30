'''
Test index page exporting.
'''

# we really need to find a proper way to do this
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])

from quarkdown import quarkify


def test_positive():
  result = quarkify.extract_quarks('''
    <!-- #QUARK live! index! -->
  ''')

  assert result["is-index"] is True, "index page not detected!"
