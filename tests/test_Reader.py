from modulefinder import IMPORT_NAME
import unittest
from unittest import result
import os,sys
from unittest import mock
from unittest.mock import Mock, patch, call
from models import IzvestajPoGradu, IzvestajPoKorisniku, IzvestajPoMesecu

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

    def test_grad_exception(self):
        with mock.patch('builtins.input', side_effect=["2", 2, 0, "0"]):
            Reader.main()
            self.assertRaises(Exception)

    def test_mesec_exception(self):
        with mock.patch('builtins.input', side_effect=["3", 2, 0, "0"]):
            Reader.main()
            self.assertRaises(Exception)

    def test_korisnik_exception(self):
        with mock.patch('builtins.input', side_effect=["1", 2, 0, "0"]):
            Reader.main()
            self.assertRaises(Exception)

    @patch('builtins.print')
    def test_grad_ispis(self, mock_print):
        Reader.posalji_zahtev = Mock()
        grad_item = IzvestajPoGradu.IzvestajGradItem(1234, "Stefan", "Kozaracka 1", 120.42)
        Reader.posalji_zahtev.return_value = IzvestajPoGradu.IzvestajGrad("Novi Sad", {"JUN":[grad_item]})
        Reader.IzvestajGradHandler("Novi Sad")
        assert mock_print.mock_calls == [call(),
                                         call(f'Potrosanja u gradu {"Novi Sad"}'),
                                         call(f'Mesec {"JUN"}'),
                                         call(f'\t{"BROJILO":<10}{"KORISNIK":24}{"ADRESA":24}{"POTROSNJA":10}'),
                                         call(f'\t{1234:<10}{"Stefan":24}{"Kozaracka 1":24}{120.42:10}'),
                                         call()]

    @patch('builtins.print')
    def test_mesec_ispis(self, mock_print):
        Reader.posalji_zahtev = Mock()
        mesec_item = IzvestajPoMesecu.IzvestajMesecItem(1234, "Stefan", "Kozaracka 1", "Novi Sad", 120.42)
        Reader.posalji_zahtev.return_value = IzvestajPoMesecu.IzvestajMesec("JUN", [mesec_item])
        Reader.IzvestajMesecHandler("JUN")
        assert mock_print.mock_calls == [call(),
                                         call(f'Potrosnja u mesecu {"JUN"}'),
                                         call(f'{"BROJILO":10}{"KORISNIK":24}{"ADRESA":24}{"GRAD":12}{"POTROSNJA":10}'),
                                         call(f'{1234:<10}{"Stefan":24}{"Kozaracka 1":24}{"Novi Sad":12}{120.42:10}'),
                                         call()]
        

    @patch('builtins.print')
    def test_korisnik_ispis(self, mock_print):
        Reader.posalji_zahtev = Mock()
        korisnik_item = IzvestajPoKorisniku.IzvestajKorisnikItem("Kozaracka 1", "Novi Sad", [("JUN", 120.42)])
        Reader.posalji_zahtev.return_value = IzvestajPoKorisniku.IzvestajKorisnik("Stefan", {1234 : korisnik_item})
        Reader.IzvestajKorisnikHandler("Stefan")
        assert mock_print.mock_calls == [call(),
                                         call(f'{"BROJILO":<10}{"KORISNIK":24}{"ADRESA":24}{"GRAD":12}'),
                                         call(f'{1234:<10}{"Stefan":24}{"Kozaracka 1":24}{"Novi Sad":12}'),
                                         call(),
                                         call(f'{"POTROSNJA":>15}'),
                                         call(f'{"JUN":5}{120.42:10}'),
                                         call()]
        





if __name__ == '__main__':
    unittest.main()