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

def ispis_korisnika():
    zahtev = ETipZahteva.GET_ALL_USERS
    vrednost = None

    odgovor = posalji_zahtev(zahtev, vrednost)
    for item in odgovor:
        brojilo, korisnik, adresa, grad = item
        print(f'{brojilo},  {korisnik:24}{adresa:24}{grad}')

def dodaj_korisnika():
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

def izbrisi_korisnika():
    zahtev = ETipZahteva.REMOVE_USER

    brojilo = input('brojilo = ')
    if not korisnik_postoji(brojilo):
        print('Korisnik ne postoji')
        return
    
    odgovor = posalji_zahtev(zahtev, brojilo)
    print(odgovor)

def korisnik_postoji(brojilo):
    zahtev = ETipZahteva.EXISTS_USER
    return_value = posalji_zahtev(zahtev, brojilo)

    return return_value

def predefinisana_baza():
    odgovor = posalji_zahtev(ETipZahteva.DB_INSERTS, None)
    print(odgovor)

def izvestaj_korisnik_handler(korisnik : str):
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

def izvestaj_mesec_handler(mesec : str):
    zahtev = ETipZahteva.MESEC

    odgovor = posalji_zahtev(zahtev, mesec)

    #ispis odgovora
    print()
    print(f'Potrosnja u mesecu {odgovor.mesec}')
    print(f'{"BROJILO":10}{"KORISNIK":24}{"ADRESA":24}{"GRAD":12}{"POTROSNJA":10}')
    for item in odgovor.items:
        print(f'{item.brojilo:<10}{item.korisnik:24}{item.adresa:24}{item.grad:12}{item.potrosnja:10}')
    print()

def izvestaj_grad_handler(grad : str):
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

def ispis_potrosnje():
    zahtev = ETipZahteva.GET_ALL_CON
    vrednost = None

    odgovor = posalji_zahtev(zahtev, vrednost)

    print(f'{"BROJILO":12}{"POTROSNJA":16}{"MESEC":6}')
    for item in odgovor:
        brojilo, potrosnja, mesec = item
        print(f'{brojilo:<12}{potrosnja:<16}{mesec:6}')


def dodaj_potrosnju(vrednost : list):
    zahtev = ETipZahteva.ADD_CON

    odgovor = dumping_buffer_zahtev(zahtev, vrednost)

    print(odgovor)

def izbrisi_potrosnju():
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
                ispis_korisnika()
            case 2:                
                dodaj_korisnika()                
            case 3:                
                izbrisi_korisnika()                
            case 4:                
                korisnik = input('Korisnik = ')
                izvestaj_korisnik_handler(korisnik)                                
            case 5:
                mesec = input('Mesec = ')
                izvestaj_mesec_handler(mesec)
            case 6:
                grad = input('Grad = ')
                izvestaj_grad_handler(grad)
            case 7:
                ispis_potrosnje()
            case 8:
                potrosnje = list()

                brojilo = input('Brojilo = ')
                potrosnja = float(input('Potrosnja = '))

                potrosnje.append((brojilo, potrosnja))
                dodaj_potrosnju(potrosnje)
            case 9:
                izbrisi_potrosnju()
            case 10:
                predefinisana_baza()
            case 0:
                os.system('cls')
                break
            case _:
                print('???')

        input('Press ENTER to continue...')
    

if __name__ == "__main__":
    main()