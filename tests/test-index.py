'''
Test index page exporting.
'''

import quarkdown as qk


def test_positive(source, encode):
  file = qk.ExportFile(file = source)
  file.content = encode('''
    <!-- #QUARK live! index! -->
  ''')

  result = qk.extract(file)

  assert result.is_index is True, "index page not detected!"
