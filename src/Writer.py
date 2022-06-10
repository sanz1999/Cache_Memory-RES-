
from ast import While
from cmath import rect
from pydoc import cli
import socket
from typing import List 

def SaljiPodatke(ID:int,potrosnja:float):
    

    try:
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        client.connect(("localhost",42500))
        client.send(ID, potrosnja)

    except: 
        print("Nije uspjelo slanje")
   

def UnosPodataka():
    try:
        id = int(input("Unesite ID korisnika: "))
        potrosnja = float(input("Unesite potrosnju za korisnika: "))
        print(f"Id : {id}  Potrosnja : {potrosnja} ")
        SaljiPodatke(id, potrosnja)
    except:
        print("Pogresan tip podatka")

    return id, potrosnja


def main():
    while True:
        id, potrosnja = UnosPodataka()
       
   
if __name__ == "__main__":
    main()


