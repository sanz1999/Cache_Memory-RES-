import unittest
import os,sys
from unittest.mock import MagicMock, Mock, patch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src import Historical
from models.ETipZahteva import ETipZahteva

cur = MagicMock()
class TestProcessRequest(unittest.TestCase):
    
    @patch('src.Historical.zahtev_korisnik')
    @patch('src.Historical.zahtev_grad')
    @patch('src.Historical.zahtev_mesec')
    def test_process_request_calls(self, mock_mesec, mock_grad, mock_korisnik):
        Historical.process_request(ETipZahteva.KORISNIK, "Ivan")
        Historical.process_request(ETipZahteva.GRAD, "Novi Sad")
        Historical.process_request(ETipZahteva.MESEC, "JUN")
        mock_korisnik.assert_called_once_with("Ivan")
        mock_grad.assert_called_once_with("Novi Sad")
        mock_mesec.assert_called_once_with("JUN")

    @patch("src.Historical.cur", cur)
    def test_zahtev_korisnik(self):
        Historical.zahtev_korisnik("Ivan")
        cur.execute.assert_called_with('''
    select k.brojilo, adresa, grad, potrosnja, mesec
    from Korisnici k, Potrosnja p
    where k.brojilo = p.brojilo and k.korisnik = ?
    ''', ("Ivan", ))  

    @patch("src.Historical.cur", cur)
    def test_zahtev_mesec(self):  
        Historical.zahtev_mesec("JUN")
        cur.execute.assert_called_with('''
    SELECT k.brojilo, korisnik, adresa, grad, potrosnja
    FROM Korisnici k, Potrosnja p
    WHERE k.brojilo = p.brojilo and mesec = ?
    ''', ("JUN", ))

    @patch("src.Historical.cur", cur)
    def test_zahtev_grad(self):  
        Historical.zahtev_grad("Novi Sad")
        cur.execute.assert_called_with('''
    SELECT k.brojilo, korisnik, adresa, potrosnja, p.mesec
    FROM Korisnici k, Potrosnja p, meseci m
    WHERE k.brojilo = p.brojilo and grad = ? and p.mesec = m.mesec
    ORDER BY m.id
    ''', ("Novi Sad", )) 
        


if __name__ == '__main__':
    unittest.main()