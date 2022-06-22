from modulefinder import IMPORT_NAME
import unittest
from unittest import result
import os,sys
from unittest import mock
from unittest.mock import Mock, patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src import Reader

class TestReader(unittest.TestCase):

    def test_main_calls(self):
        with mock.patch('builtins.input', side_effect=["2", "JUN", "0", "1", "Ivan", "0", "3", "Novi Sad", "0", "0"]):
            Reader.IzvestajGradHandler = Mock()
            Reader.IzvestajMesecHandler = Mock()
            Reader.IzvestajKorisnikHandler = Mock()
            Reader.main()
            Reader.IzvestajMesecHandler.assert_called_once_with("JUN")
            Reader.IzvestajGradHandler.assert_called_once_with("Novi Sad")
            Reader.IzvestajKorisnikHandler.assert_called_once_with("Ivan")


if __name__ == '__main__':
    unittest.main()