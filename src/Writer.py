import socket
import pickle
import os,sys
import string

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.ConnectionParams import HOST,  W_PORT

def unos(poruka:string,tip:type):
    try:
        return tip(input(poruka))
    except Exception:
        raise ValueError(f"Unos nije tipa: {tip.__name__}")

def povezi_se(): # pragma: no cover
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        client.connect((HOST,W_PORT))
    except Exception:
        raise ConnectionError
    else:
        return client


def salji_podatke(id:int,potrosnja:float): # pragma: no cover
    try:
        client = povezi_se()
        data = id,potrosnja
        data = pickle.dumps(data)
        client.send(data)
    except ConnectionError: 
        print("Nije moguce uspostavljanje konekcije")
    except Exception as e:
        print(e)
    else:
        print("Podatak uspesno poslat Dumping Buffer-u")
   
def unos_podataka():
    try:

        id_korisnika = unos("Unesite ID korisnika:",int)
        potrosnja = unos("Unesite potrosnju za korisnika: ",float)
        print(f"Id : {id_korisnika}  Potrosnja : {potrosnja} ")
    except ValueError as e:
        print(str(e))
    else:
        return id_korisnika, potrosnja

def main(): # pragma: no cover
    while True:
        try:
            id_korisnika, potrosnja = unos_podataka()
        except TypeError:
            print("Ponovite celokupan unos")
        except KeyboardInterrupt:
            print("\nWriter se zatvara")
            return 
        else:
            salji_podatke(id_korisnika, potrosnja)       

   
if __name__ == "__main__": # pragma no cover
    main()




