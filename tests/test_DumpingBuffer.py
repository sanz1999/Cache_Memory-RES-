from modulefinder import IMPORT_NAME
import unittest
from unittest import result
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.DumpingBuffer import *

class TestDumpingBuffer(unittest.TestCase):

    def test_UslovZaSlanjePodataka(self):
        result = UslovZaSlanjePodataka()
        self.assertFalse(result)
#        self.assertEqual(result,True)
        self.assertEqual(result,False)

if __name__ == '__main__':
    unittest.main()