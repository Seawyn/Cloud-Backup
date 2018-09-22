#Computers' Networks Project
#Group 17

import socket
import sys

def main():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(len(sys.argv) == 3 and (isinstance(sys.argv[2], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
    server_adress = ('localhost', CSport)
    sckt.bind(server_adress)
    sckt.listen(1)
    while True:
        connection, client_adress = sckt.accept()
        try:
            while True:
                data = connection.recv(16)
                print(data)
                if data:
                    connection.sendall(data)
                else:
                    break
        finally:
            connection.close()
    return 0


main()
