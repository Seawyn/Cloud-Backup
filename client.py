#Computers' Networks Project
#Group 17

import socket
import sys

def main():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(len(sys.argv) == 4):
        CSname = input("CS name: ")
        CSport = input("Port: ")
    elif(len(sys.argv) == 3 and isinstance(sys.argv[2], str)):
        CSname = input("CS name: ")
    elif(len(sys.argv) == 3 and isinstance(sys.argv[2], int)):
        CSport = input("port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
    server_adress = ('localhost', CSport)
    user = input("User: ")
    password = input("Password: ")
    sckt.connect(server_adress)
    try:
        message = user + " " + password
        sckt.sendall(message.encode())
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sckt.recv(128)
            amount_received += len(data)
            print(data.decode())
    finally:
        sckt.close()
    return 0

main()
