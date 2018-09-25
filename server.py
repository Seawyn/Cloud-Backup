#Computers' Networks Project
#Group 17

import socket
import sys

def main():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users = []
    if(len(sys.argv) == 3 and (isinstance(sys.argv[2], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
    server_adress = ('localhost', CSport)
    sckt.bind(server_adress)
    sckt.listen(1)
    success = "user added"
    while True:
        connection, client_adress = sckt.accept()
        try:
            while True:
                data = connection.recv(128)
                data = data.decode()
                data = data.split()
                users += [data]
                if data:
                    connection.sendall(success.encode())
                    print(users)
                else:
                    break
        finally:
            connection.close()

    return 0


main()
