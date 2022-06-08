from ctypes import sizeof
import socket, pickle, sys

HOST = '127.0.0.1'
DB_PORT = 42502
R_PORT = 42501

class Objekat():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    def __str__(self) -> str:
        return f'{self.x},{self.y}'
    

def main(): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, R_PORT))

        O = Objekat(5,34)
        print(sys.getsizeof(O))

        s.sendall(pickle.dumps(O))
        
        data = pickle.loads(s.recv(1024)) 

        s.sendall(pickle.dumps(O))
        
        data = pickle.loads(s.recv(1024)) 

    #print(f"Received {data}")

    print('Hello')
    

if __name__ == "__main__":
    main()