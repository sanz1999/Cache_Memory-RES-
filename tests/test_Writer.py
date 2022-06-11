import imp
from modulefinder import IMPORT_NAME
import unittest
from unittest import result
from unittest.mock import patch,Mock
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.Writer import *

class TestWriter(unittest.TestCase):

      def test_UnosPodataka():
        pass 

      def test_SaljiPodatke():
        pass

    

if __name__ == '__main__':
    unittest.main()
    