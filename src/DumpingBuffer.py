from collections import deque
import socket,pickle,asyncio,os,sys
from typing import final 

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from models.ConnectionParams import HOST, DB_PORT, W_PORT

DATA_SIZE = 1024
BUFFER_SIZE = 7

red = deque()

def ListaZaSlanje():

    listaZaSlanje =[]

    for i in range(BUFFER_SIZE):
        listaZaSlanje.append(red.popleft())

    return ListaZaSlanje

def PosaljiPodatkeHistorical():
    historicalSocket = socket.socket((socket.AF_INET,socket.SOCK_STREAM))
    try:
        historicalSocket.connect(HOST,DB_PORT)
    except:
        print("Povezivanje na Historical neuspesno")
    else:
        lista = ListaZaSlanje()
        data_string = pickle.dumps(lista)
        historicalSocket.send(data_string)
        print("Uspesno poslato")
    
def pozalji():
    lista = ListaZaSlanje()
    print("Skinuto 7 iz reda")
    

def UslovZaSlanjePodataka():
    if len(red) >= BUFFER_SIZE:
        return True
    else :
        return False

async def SaljiPodatke():
    while True:
        if UslovZaSlanjePodataka():
            pozalji()
            #PosaljiPodatkeHistorical()
        else:
            print("ziv sam 2 sekunde")
            await asyncio.sleep(2)
        
def PrimiPodatke(data):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,W_PORT))
    server.listen()


async def main():
    asyncio.create_task(SaljiPodatke())

    try:
        dumpingbufferSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        dumpingbufferSocket.bind((HOST,W_PORT))
        dumpingbufferSocket.listen()
        print("Kreirana")
        while True:
            writer,address = dumpingbufferSocket.accept()
            print(f"Povezan Writer adresa:{address}")
            data = writer.recv(DATA_SIZE)
            data = pickle.loads(data)
            red.append(data)
            print(type(data))
            print(data)
            print(f"Br elem u que:{len(red)}")
            
            
    except KeyboardInterrupt:                           #omogucava Ctrl+C prekid programa
        print("Caught keyboard interrupt, exiting")
    finally:
        dumpingbufferSocket.close()
        pass



if __name__ == "__main__":
    asyncio.run(main())

