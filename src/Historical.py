import sqlite3
import socket, pickle, selectors, types
from HistoricalAdmin import Objekat

#Instanca selektora za asinhroni rad soketa
sel = selectors.DefaultSelector()

#Konekcija sa SQLite DataBase
conn = sqlite3.connect('../data/dataBase.db')
cur = conn.cursor()

#Pravljenje Tabela u slucaju da ne postoje
cur.executescript('''
CREATE TABLE IF NOT EXISTS "Korisnici" (
    "brojilo"	INTEGER NOT NULL UNIQUE,
    "ime"	TEXT NOT NULL,
    "adresa"	TEXT NOT NULL UNIQUE,
    "grad"	TEXT NOT NULL,
    PRIMARY KEY("brojilo")
);
CREATE TABLE IF NOT EXISTS "Potrosnja" (
    "id"	INTEGER,
    "brojilo"	INTEGER,
    "potrosnja"	REAL NOT NULL CHECK("potrosnja" > 0),
    "mesec"	TEXT NOT NULL UNIQUE,
    PRIMARY KEY("id" AUTOINCREMENT),
    FOREIGN KEY("brojilo") REFERENCES "Korisnici"("brojilo")
);
''')

#Parametri soketa, verovatno bi trebalo da ih prebacimo u neki fajl sa globalnim konstantama
HOST = '127.0.0.1'
DB_PORT = 42502
R_PORT = 42501

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {pickle.loads(data.outb)} to {data.addr}")
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def main():    
    
    data_buffer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reader_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    data_buffer_socket.bind((HOST, DB_PORT))
    reader_socket.bind((HOST, R_PORT))

    data_buffer_socket.listen()
    reader_socket.listen()

    data_buffer_socket.setblocking(False)
    reader_socket.setblocking(False)

    sel.register(data_buffer_socket, selectors.EVENT_READ, data=None)
    sel.register(reader_socket, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=0)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:                           #omogucava Ctrl+C prekid programa
        print("Caught keyboard interrupt, exiting")
    finally:
        sel.close()

if __name__ == "__main__":
    main()