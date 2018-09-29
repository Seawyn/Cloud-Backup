#Computers' Networks Project
#Group 17

import socket
import sys

def main():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users = {}
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
                data = connection.recv(1024)
                data = data.decode()
                data = data.split()
                if data:
                    if(data[1] not in users):
                        users[data[1]] = data[2]
                        message = "AUR NEW"
                        print("New user: " + data[1])
                    else:
                        if(users[data[1]] == data[2]):
                            print("User: " + data[1])
                            message = "AUR OK"
                        else:
                            message = "AUR NOK"
                    connection.sendall(message.encode())
                else:
                    break
        finally:
            connection.close()

    return 0


main()
