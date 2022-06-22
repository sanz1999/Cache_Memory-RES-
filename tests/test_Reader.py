from modulefinder import IMPORT_NAME
import unittest
from unittest import result
import os,sys
from unittest import mock
from unittest.mock import Mock, patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src import Reader

class TestDumpingBuffer(unittest.TestCase):

    def test_unos(self):
        with mock.patch('builtins.input', side_effect=[2]):
            Reader.IzvestajMesecHandler = Mock()
            Reader.main()
            Reader.IzvestajMesecHandler.assert_called_once()


if __name__ == '__main__':
    unittest.main()