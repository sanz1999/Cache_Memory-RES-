from modulefinder import IMPORT_NAME
import unittest
from unittest import result
from unittest import mock
from unittest.mock import patch,Mock,MagicMock,call
import os,sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src import Writer


class TestWriter(unittest.TestCase):

    @patch('src.Writer.unos')
    def test_unos_podataka_ok(self,mock_unos):
        mock_unos.side_effect = [2,3]
        self.assertEqual(Writer.unos_podataka(),(2,3))

    @patch('builtins.print')
    @patch('src.Writer.input')
    def test_unos_podataka_not_ok(self, mock_unos, mock_print):
        mock_unos.side_effect = ["dva", 3]
        Writer.unos_podataka()
        mock_print.assert_called_with(f"Unos nije tipa: {int.__name__}")

    @patch('src.Writer.input')
    def test_unos(self,mock_unos):
        mock_unos.return_value = 2
        self.assertEqual(Writer.unos("",int),2)
        mock_unos.return_value = 2.3
        self.assertRaises(TypeError,Writer.unos("",int))



    
if __name__ == '__main__':
    unittest.main()