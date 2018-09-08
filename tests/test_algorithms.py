from copy import deepcopy
import unittest
import os

from wfst import TropicalWeight
from wfst.io import from_fsm_format, to_fsm_format_walk
from wfst.algo import nbest

from .utils import walk_all

class TestAlgorithms(unittest.TestCase):

    def test_nbest(self):
        test_dir = os.path.join(os.path.dirname(__file__), "testdata")
        for test_sample in range(1, 2):
            test_sample = str(test_sample).zfill(2)
            test_input_infn = os.path.join(test_dir, "test_{}.txt".format(test_sample))
            test_output_infn = os.path.join(test_dir, "test_{}_nbest_{{}}_tropical.txt".format(test_sample))
            #GIVEN Wfst with known nbest paths
            with open(test_input_infn) as infh:
                wfst = from_fsm_format(infh, semiring=TropicalWeight)
            for n in range(1, 6):
                #WHEN
                nbest_wfst = nbest(deepcopy(wfst), n)
                #THEN
                with open(test_output_infn.format(n)) as infh:
                    expected_nbest_wfst = from_fsm_format(infh, semiring=TropicalWeight)
                a = walk_all(nbest_wfst)
                b = walk_all(expected_nbest_wfst)
                self.assertEqual(a, b)
 
            
if __name__ == '__main__':
    unittest.main()
