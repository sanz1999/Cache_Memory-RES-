from ast import arg
from collections import deque
from csv import writer
from dataclasses import replace
from inspect import ArgSpec
from logging import exception
import socket
import pickle
import os
import sys
import threading
import select
import time
from time import sleep

#Dodavanje putanja u path, kako bi moglo da se pristupa drugim folderima i modulima
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
#Importovanje zajednickih promenljivih koje definisu parametre povezivanja
from models.ConnectionParams import HOST, DB_PORT, W_PORT
from models.ETipZahteva import ETipZahteva

#Velicina podatka koji primamo prilikom komunikacije
DATA_SIZE = 1024

#Velicina koja odredjuje kolicinu podatak koji se preuzimaju iz reda i salju historical komponenti
BUFFER_SIZE = 7

#Interna FIFO memorijska struktura


def napravi_listu_za_slanje_podataka(red:deque):
    lista =[]
    i=0
    while i<BUFFER_SIZE:
        lista.append(red.popleft()) #istovremeno uklanjanje iz reda i ubacivanje u listu za slanje
        i+=1
    return lista

def uslov_za_slanje_podataka(red:deque):
    if len(red) >= BUFFER_SIZE:
        return True
    else :
        return False

def preuzmi_podatke(writer:socket): # pragma: no cover
    data = writer.recv(DATA_SIZE)
    data = pickle.loads(data)
    writer.close()
    return data

def upisi_u_red(data:tuple,red:deque):
    red.append(data)
    print(f"Upisano u red. Trenutni broj {len(red)}")

def uspostavi_dolaznu_konekciju(): # pragma: no cover
    dumpingbuffer_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    dumpingbuffer_socket.bind((HOST,W_PORT))
    dumpingbuffer_socket.listen()
    writer,address = dumpingbuffer_socket.accept()
    print(f"Povezan Writer adresa:{address}")
    return writer

def uspostavi_odlaznu_konekciju(): # pragma: no cover
    historical_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    historical_socket.connect((HOST,DB_PORT))
    return historical_socket

def posalji_podatke(red:deque): # pragma: no cover
    try:
        historical = uspostavi_odlaznu_konekciju()
    except ConnectionError:
        print("Nije moguca konekcija na Historical")
    else:       
        lista = napravi_listu_za_slanje_podataka(red)
        data_string = pickle.dumps((ETipZahteva.ADD_CON, lista))
        historical.send(data_string)
        print("Uspesno poslato")

    
def proces_primanja_podataka(red:deque): # pragma: no cover
    while True:
        try:
            writer = uspostavi_dolaznu_konekciju()
        except Exception as e:
            print(e)
        else:
            data = preuzmi_podatke(writer)
            upisi_u_red(data,red)
            
        

def proces_slanja_podataka(red:deque): # pragma: no cover
    while True:
        if uslov_za_slanje_podataka(red):
            posalji_podatke(red)
            sleep(2)
        else:
            sleep(2)
            

def pokreni_tredove(lista:list): # pragma: no cover
    for tred in lista:
        try:
            tred.start()
        except Exception as e:
            print(f"Proces: {tred.name} nije pokrenut")
            print(e)
        else:
            print(f"Proces: {tred.name} pokrenut")

def kreiraj_tredove(red:deque):
    tredovi = []
    tredovi.append(threading.Thread(name="Listener",target=proces_primanja_podataka,args=(red,),daemon=True))
    tredovi.append(threading.Thread(name="Sender",target=proces_slanja_podataka,args=(red,),daemon=True))
    return tredovi

def main(): # pragma: no cover
    red = deque()
    tredovi = kreiraj_tredove(red)
    pokreni_tredove(tredovi)
    print("DumpingBuffer pokrenut") 
    a= input()
    print(a)
    print("DumpingBuffer se zatvara")

if __name__ == "__main__": # pragma: no cover
    main()
