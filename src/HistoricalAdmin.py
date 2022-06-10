from calendar import month
from ctypes import sizeof
from datetime import date
import socket, pickle, sys, os

#Neka glupost da bi mogo da importujem iz modela
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.ConnectionParams import HOST, DB_PORT, R_PORT
from models.ETipZahteva import ETipZahteva
    
def dumping_buffer_zahtev(zahtev, vrednost):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, DB_PORT))
        data = bytes()

        pack = pickle.dumps((zahtev, vrednost))
        client_socket.sendall(pack)
        
        while True:
            recv_data = client_socket.recv(4096)
            if not recv_data:
                break
            data += recv_data

        return pickle.loads(data)

def posalji_zahtev(zahtev, vrednost):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, R_PORT))
        data = bytes()

        pack = pickle.dumps((zahtev, vrednost))
        client_socket.sendall(pack)
        
        while True:
            recv_data = client_socket.recv(4096)
            if not recv_data:
                break
            data += recv_data

        return pickle.loads(data)

def IspisKorisnika():
    zahtev = ETipZahteva.GET_ALL_USERS
    vrednost = None

    odgovor = posalji_zahtev(zahtev, vrednost)
    for item in odgovor:
        brojilo, korisnik, adresa, grad = item
        print(f'{brojilo},  {korisnik:24}{adresa:24}{grad}')

def DodajKorisnika():
    zahtev = ETipZahteva.ADD_USER

    try:
        brojilo = int(input('brojilo = '))
    except ValueError:
        print('Brojilo mora biti broj')
        input('Press ENTER to continue...')
        return
        
    korisnik = input('korisnik = ')
    adresa  = input('adresa = ')
    grad = input('grad = ')
    vrednost = (brojilo, korisnik, adresa, grad)

    odgovor = posalji_zahtev(zahtev, vrednost)
    print(odgovor)

def IzbrisiKorisnika():
    zahtev = ETipZahteva.REMOVE_USER

    brojilo = input('brojilo = ')
    if not KorisnikPostoji(brojilo):
        print('Korisnik ne postoji')
        return
    
    odgovor = posalji_zahtev(zahtev, brojilo)
    print(odgovor)

def KorisnikPostoji(brojilo):
    zahtev = ETipZahteva.EXISTS_USER
    return_value = posalji_zahtev(zahtev, brojilo)

    return return_value

def PredefinisanaBaza():
    odgovor = posalji_zahtev(ETipZahteva.DB_INSERTS, None)
    print(odgovor)

def IzvestajKorisnikHandler(korisnik : str):
    zahtev = ETipZahteva.KORISNIK

    odgovor = posalji_zahtev(zahtev, korisnik)

    #ispis odgovora
    print()
    for key, value in (odgovor.items).items():
        print(f'{"BROJILO":<10}{"KORISNIK":24}{"ADRESA":24}{"GRAD":12}')
        print(f'{key:<10}{odgovor.korisnik:24}{value.adresa:24}{value.grad:12}')
        print()
        print(f'{"POTROSNJA":>15}')   
        for item in value.potrosnje:
            print(f'{item[0]:5}{item[1]:10}')
        print()

def IzvestajMesecHandler(mesec : str):
    zahtev = ETipZahteva.MESEC

    odgovor = posalji_zahtev(zahtev, mesec)

    #ispis odgovora
    print()
    print(f'Potrosnja u mesecu {odgovor.mesec}')
    print(f'{"BROJILO":10}{"KORISNIK":24}{"ADRESA":24}{"GRAD":12}{"POTROSNJA":10}')
    for item in odgovor.items:
        print(f'{item.brojilo:<10}{item.korisnik:24}{item.adresa:24}{item.grad:12}{item.potrosnja:10}')
    print()

def IzvestajGradHandler(grad : str):
    zahtev = ETipZahteva.GRAD

    odgovor = posalji_zahtev(zahtev, grad)

    #ispis odgovora
    print()
    print(f'Potrosanja u gradu {odgovor.grad}')
    
    for key, value in (odgovor.items).items():
        print(f'Mesec {key}')
        print(f'\t{"BROJILO":<10}{"KORISNIK":24}{"ADRESA":24}{"POTROSNJA":10}')        
        for item in value:
            print(f'\t{item.brojilo:<10}{item.korisnik:24}{item.adresa:24}{item.potrosnja:10}')
        print()

def IspisPotrosnje():
    zahtev = ETipZahteva.GET_ALL_CON
    vrednost = None

    odgovor = posalji_zahtev(zahtev, vrednost)

    print(f'{"BROJILO":12}{"POTROSNJA":16}{"MESEC":6}')
    for item in odgovor:
        brojilo, potrosnja, mesec = item
        print(f'{brojilo:<12}{potrosnja:<16}{mesec:6}')


def DodajPotrosnju(vrednost : list):
    zahtev = ETipZahteva.ADD_CON

    odgovor = dumping_buffer_zahtev(zahtev, vrednost)

    print(odgovor)

def IzbrisiPotrosnju():
    raise NotImplementedError

def main(): 
    while True:
        os.system('cls')

        print('Moguci zahtevi : ')
        print('1. Svi korisnici')
        print('2. Dodaj korisnika')
        print('3. Izbrisi korisnika')
        print('4. Izvestaj po korisniku')
        print('5. Izvestaj po mesecu')
        print('6. izvestaj po gradu')
        print('7. Sve potrosnje')
        print('8. Dodaj potrosnju')
        print('9. Izbrisi potrosnju')

        print('10. Ocitaj predefinisanu bazu')
        print('0. za izlaz')

        answer = int(input())

        match answer:
            case 1:
                try:
                    IspisKorisnika()
                except Exception as e:
                    print(e)
            case 2:
                try:
                    DodajKorisnika()
                except Exception as e:
                    print(e)
            case 3:
                try:
                    IzbrisiKorisnika()
                except Exception as e:
                    print(e)
            case 4:
                try:
                    korisnik = input('Korisnik = ')
                    IzvestajKorisnikHandler(korisnik)
                except Exception as e:
                    print(e)                
            case 5:
                mesec = input('Mesec = ')
                try:
                    IzvestajMesecHandler(mesec)
                except Exception as e:
                    print(e)
            case 6:
                try:
                    grad = input('Grad = ')
                    IzvestajGradHandler(grad)
                except Exception as e:
                    print(e)
            case 7:
                try:
                    IspisPotrosnje()
                except Exception as e:
                    print(e)
            case 8:
                potrosnje = list()

                brojilo = input('Brojilo = ')
                potrosnja = float(input('Potrosnja = '))

                potrosnje.append((brojilo, potrosnja))
                try:
                    DodajPotrosnju(potrosnje)
                except Exception as e:
                    print(e)
            case 9:
                try:
                    IzbrisiPotrosnju()
                except Exception as e:
                    print(e)
            case 10:
                try:
                    PredefinisanaBaza()
                except Exception as e:
                    print(e)
            case 0:
                os.system('cls')
                break
            case _:
                print('???')

        input('Press ENTER to continue...')
    

if __name__ == "__main__":
    main()