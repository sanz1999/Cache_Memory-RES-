
import socket, pickle, os, sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.ConnectionParams import HOST,  W_PORT


def SaljiPodatke(ID:int,potrosnja:float):
    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        client.connect((HOST,W_PORT))
        data = ID,potrosnja
        print(data)
        data = pickle.dumps(data)
        print(type(data))
        
        client.send(data)

    except: 
        print("Nije uspelo slanje")
   

def UnosPodataka():
    try:
        id = int(input("Unesite ID korisnika: "))
        potrosnja = float(input("Unesite potrosnju za korisnika: "))
        print(f"Id: {id}  Potrosnja: {potrosnja} ")
    except:
        print("Pogresan tip podatka")
    return id, potrosnja

 
def main():
    while True:
        id, potrosnja = UnosPodataka()
        SaljiPodatke(id, potrosnja)
       
   
if __name__ == "__main__":
    main()


