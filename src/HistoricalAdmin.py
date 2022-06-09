from ctypes import sizeof
import socket, pickle, sys, os

#Neka glupost da bi mogo da importujem iz modela
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.ConnectionParams import HOST, DB_PORT, R_PORT
from models.ETipZahteva import ETipZahteva
    
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

def IzvestajKorisnikHandler():
    zahtev = ETipZahteva.KORISNIK

    korisnik = input('Korisnik = ')

    odgovor = posalji_zahtev(zahtev, korisnik)
    print()
    print(odgovor[0])
    print(f'Podatci :\n\tbrojilo : {odgovor[1].brojilo}\n\tadresa : {odgovor[1].adresa}, {odgovor[1].grad}')
    print('Potrosnje : ')
    for item in odgovor[1].lista:
        print(f'\t{item[0]} : {item[1]}')
    print()

def main(): 
    while True:
        os.system('cls')

        print('Moguci zahtevi : ')
        print('1. Svi korisnici')
        print('2. Dodaj korisnika')
        print('3. Izbrisi korisnika')
        print('4. Izvestaj po korisniku')
        print('9. Ocitaj predefinisanu bazu')
        print('0. za izlaz')

        answer = int(input())

        match answer:
            case 1:
                IspisKorisnika()

            case 2:
                DodajKorisnika()

            case 3:
                IzbrisiKorisnika()
            case 4:
                IzvestajKorisnikHandler()

            case 9:
                PredefinisanaBaza()

            case 0:
                os.system('cls')
                break

            case _:
                print('???')

        input('Press ENTER to continue...')
    

if __name__ == "__main__":
    main()