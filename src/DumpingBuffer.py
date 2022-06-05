from collections import deque
import socket
import pickle
import asyncio


DATA_SIZE = 2048
BUFFER_SIZE = 7
LOCALHOST = socket.gethostbyname(socket.gethostname)
DUMPINGBUFFER_PORT = 42500
HISTORICAL_PORT = 42502
#ovde ce ici implementacija queua

red = deque()

def ListaZaSlanje():
    listaZaSlanje =[]

    for i in range(BUFFER_SIZE):
        listaZaSlanje.append(red.popleft())

    return ListaZaSlanje

def PosaljiPodatkeHistorical():
    historicalSocket = socket.socket((socket.AF_INET,socket.SOCK_STREAM))
    try:
        historicalSocket.connect(LOCALHOST,HISTORICAL_PORT)
    except:
        print("Povezivanje na Historical neuspesno")
    else:
        lista = ListaZaSlanje()
        data_string = pickle.dumps(lista)
        historicalSocket.send(data_string)
        print("Uspesno poslato")
    
    
def UslovZaSlanjePodataka():
    if len(red) >= 7:
        return True
    else :
        return False

async def SaljiPodatke():
    while True:
        if UslovZaSlanjePodataka():
            PosaljiPodatkeHistorical()
        else:
            await asyncio.sleep(2)
        
def PrimiPodatke(data):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((LOCALHOST,DUMPINGBUFFER_PORT))
    server.listen()


async def main():
    asyncio.create_task(SaljiPodatke())
    while True:
        dumpingbufferSocket =  socket.socket((socket.AF_INET,socket.SOCK_STREAM))
        dumpingbufferSocket.bind((LOCALHOST,DUMPINGBUFFER_PORT))
        dumpingbufferSocket.listen()
        writer,address = dumpingbufferSocket.accept()
        print(f"Povezan Writer adresa:{address}")
        data = writer.recv(DATA_SIZE)
        dumpingbufferSocket.close()
        data = pickle.loads(data)
        red.append(data)
        print("Podaci uspesno upisani u queue")
        

        
    


if __name__ == "__main__":
    asyncio.run(main())

