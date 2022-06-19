import pickle
import sys,os
from random import choices
import socket

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.ConnectionParams import HOST, R_PORT
from models.IzvestajPoGradu import *
from models.IzvestajPoKorisniku import *
from models.IzvestajPoMesecu import *
from models.ETipZahteva import ETipZahteva


#konekcija sa soketom i slanje zahtjeva
#slanje zahtjeva
#funkcije za ispis
#sa tipom zahtjeva je proslijedjen parametar po kome se pretrazuje(za sva 3 tipa)


def menu():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("localhost", 42501))
    print("Odaberite opciju za ispis")
    choices={
        1: "Ispis po mesecu",
        2: "Ispis po korisniku",
        3: "Ipsis po gradu"
    }

    for i in choices.keys():
        print(f"{i} - {choices[i]}")
    arg = int((input("Unesite redni broj opcije:")))
    fun = choices.get(arg, -1)
    while fun == -1:
        print("Odabrali ste nepostojecu opciju!")
        menu()

    else:
        
        print(f"Odabrali ste opciju {fun}")
        if fun == 1:
            tipzahteva = ETipZahteva.MESEC
            mesec = ((input("Unesite mesec:")))
            client.send(tipzahteva, mesec)
        if fun == 2:
            tipzahteva = ETipZahteva.KORISNIK
            korisnik = int((input("Unesite id korisnika:")))
            client.send(tipzahteva, korisnik)
        if fun == 3:
            tipzahteva = ETipZahteva.GRAD  
            grad = ((input("Unesite naziv grada:")))
            client.send(tipzahteva, grad)  
    return client.recv(1024)

def ispis(objekat):
    if type(objekat) == tuple(str, list(IzvestajPoMesecu)): 
        print(objekat[0])
        for item in objekat[1]:            
            print("\t\t", end='')
            print(f"{item.brojilo}, {item.ime}, {item.prezime}, {item.adresa}, {item.grad}, {item.potrosnja}")
    
    
    elif type(objekat) ==  tuple(int, IzvestajPoKorisniku): 
        print(objekat[0])
        for potrosnja in objekat[1].lista:   
           print(potrosnja[0] + potrosnja[1])
        print(objekat[1].ime, objekat[1].prezime, objekat[1].adresa, objekat[1].grad)         
    
    
    elif type(objekat) == tuple(str, dict(str, list(IzvestajPoGradu))): 
        #ime grada
        print(objekat[0])
        #mesec
        for mesec in objekat[1].keys:
            print(mesec)
            #sve u tom mesecu
            for item in objekat[1][mesec]:
                print(item.brojilo, item.ime, item.prezime, item.potrosnja)
 
def main():
    while True:
        objekat = menu()
        ispis(objekat)
    

if __name__ == "__main__":
    main()



