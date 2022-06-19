from modulefinder import IMPORT_NAME
import unittest
from unittest import result
import os,sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.Reader import *



if __name__ == '__main__':
    unittest.main()