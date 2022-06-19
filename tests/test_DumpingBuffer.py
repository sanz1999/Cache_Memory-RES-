from collections import deque
from ctypes import WinError
from modulefinder import IMPORT_NAME
import unittest
from unittest import result
from unittest.mock import patch,Mock
import os,sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src import DumpingBuffer

class TestDumpingBuffer(unittest.TestCase):

    def napuni_red(broj:int):
        red = deque()
        i=0
        while i<broj:
            red.append((2,2.3))
            i+=1
        return red

    def test_napravi_listu_za_slanje_podataka(self):
        red =TestDumpingBuffer.napuni_red(7)
        self.assertEqual( list(red),DumpingBuffer.napravi_listu_za_slanje_podataka(red))
        red =TestDumpingBuffer.napuni_red(10)
        self.assertNotEqual( list(red),DumpingBuffer.napravi_listu_za_slanje_podataka(red))


    def test_uslov_za_slanje_podataka(self):
        red =TestDumpingBuffer.napuni_red(7)
        self.assertEqual(True,DumpingBuffer.uslov_za_slanje_podataka(red))
        DumpingBuffer.napravi_listu_za_slanje_podataka(red)
        self.assertEqual(False,DumpingBuffer.uslov_za_slanje_podataka(red))
        red =TestDumpingBuffer.napuni_red(2)
        self.assertEqual(False,DumpingBuffer.uslov_za_slanje_podataka(red))

     

if __name__ == '__main__':
    unittest.main()