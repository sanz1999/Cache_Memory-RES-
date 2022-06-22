from collections import deque
from ctypes import WinError
from modulefinder import IMPORT_NAME
import unittest
from unittest import result
from unittest.mock import patch,Mock, ANY
import threading
import os,sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src import DumpingBuffer

class TestDumpingBuffer(unittest.TestCase):

    @staticmethod
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

    @patch('builtins.print')
    def test_upisi_u_red(self, mock_print):
        red = self.napuni_red(5)
        DumpingBuffer.upisi_u_red((1,2,3), red)
        mock_print.assert_called_with(f"Upisano u red. Trenutni broj {len(red)}")
     
    def test_kreiraj_tredove(self):
        red = self.napuni_red(5)
        self.assertEqual(len(DumpingBuffer.kreiraj_tredove(red)),2)

if __name__ == '__main__':
    unittest.main()