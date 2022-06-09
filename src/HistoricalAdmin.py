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

def IzvestajMesecHandler():
    zahtev = ETipZahteva.MESEC

    mesec = input('Mesec = ')

    odgovor = posalji_zahtev(zahtev, mesec)

    print()
    print(f'Potrosnja u mesecu {odgovor[0]}')
    print(f'{"BROJILO":10}{"KORISNIK":24}{"ADRESA":24}{"GRAD":12}{"POTROSNJA":10}')
    for item in odgovor[1].items:
        print(f'{item.brojilo:<10}{item.korisnik:24}{item.adresa:24}{item.grad:12}{item.potrosnja:10}')
    print()

def IzvestajGradHandler():
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
        print('9. Ocitaj predefinisanu bazu')
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
                    IzvestajKorisnikHandler()
                except Exception as e:
                    print(e)                
            case 5:
                try:
                    IzvestajMesecHandler()
                except Exception as e:
                    print(e)
            case 6:
                try:
                    IzvestajGradHandler()
                except Exception as e:
                    print(e)
            case 9:
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