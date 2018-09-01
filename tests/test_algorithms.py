import unittest
import os
from glob import glob

from wfst import TropicalWeight
from wfst.io import from_fsm_format, to_fsm_format_walk


class TestAlgorithms(unittest.TestCase):

    def test_nbest(self):
        for test_infn in glob(os.path.join(os.path.dirname(__file__), "test_??.txt")):
            print(test_infn)
            with open(test_infn) as infh:
                wfst = from_fsm_format(infh, semiring=TropicalWeight)
        for line in to_fsm_format_walk(wfst):
            print(line)

            
if __name__ == '__main__':
    unittest.main()
