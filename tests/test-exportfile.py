'''
Test `ExportFile` operations.
'''

import quarkdown as qk


def test_export(file):
  result = qk.extract(file)
  assert isinstance(result, qk.ExportFile)
