from http import client
import socket


def main():
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("localhost", 42501))
    

if __name__ == "__main__":
    main()



