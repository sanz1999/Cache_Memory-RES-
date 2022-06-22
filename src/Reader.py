import pickle, os, sys
import socket

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.IzvestajPoGradu import *
from models.IzvestajPoKorisniku import *
from models.IzvestajPoMesecu import *

from models.ConnectionParams import HOST, DB_PORT, R_PORT
from models.ETipZahteva import ETipZahteva

def main():
     while True:
        os.system('cls')

        print('Moguci zahtevi : ')
        print('1. Izvestaj po korisniku')
        print('2. Izvestaj po mesecu')
        print('3. izvestaj po gradu')
       
        print('0. za izlaz')

        answer = int(input())

        match answer:   
            case 1:
                try:
                    korisnik = input('Korisnik = ')
                    IzvestajKorisnikHandler(korisnik)
                except Exception as e:
                    print(e)                
            case 2:
                mesec = input('Mesec = ')
                try:
                    IzvestajMesecHandler(mesec)
                except Exception as e:
                    print(e)
            case 3:
                try:
                    grad = input('Grad = ')
                    IzvestajGradHandler(grad)
                except Exception as e:
                    print(e)
            
            case 0:
                os.system('cls')
                break
            case _:
                print('???')

        
        input('Press ENTER to continue...')  



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

def posalji_zahtev(zahtev, vrednost): # pragma: no cover
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
    

if __name__ == "__main__":
    main()



