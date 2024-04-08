# this file is for manual debugging
import sys
sys.path[0] = "/".join(sys.path[0].split("/")[:-1])
import quarkify


quarkify.test_data_single()
quarkify.test_data_multi()
