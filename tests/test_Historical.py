import unittest
import os,sys
from unittest.mock import Mock

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src import Historical
from models.ETipZahteva import ETipZahteva

class TestProcessRequest(unittest.TestCase):
    
    def test_process_request(self):
        Historical.zahtev_korisnik = Mock()
        Historical.zahtev_grad = Mock()
        Historical.zahtev_mesec = Mock()
        Historical.process_request(ETipZahteva.KORISNIK, "Ivan")
        Historical.process_request(ETipZahteva.GRAD, "Ivan")
        Historical.zahtev_korisnik.assert_called_once()
        Historical.zahtev_grad.assert_called_once()
        Historical.zahtev_mesec.assert_not_called()


if __name__ == '__main__':
    unittest.main()