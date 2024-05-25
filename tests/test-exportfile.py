'''
Test `ExportFile` operations.
'''

import quarkdown as qk


def test_export(source, encode):
  file = qk.ExportFile(file = source)
  file.content = encode("test")
  
  result = qk.extract(file)
  assert isinstance(result, qk.ExportFile)
