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

    #Sending user id (succeeds if server replies with 'accepted', fails otherwise)
    message = user
    sckt.send(message)
    amount_received = 0
    amount_expected = len('accepted')
    data = sckt.recv(22)
    if (data != 'accepted'):
        print(data)
        sckt.close()
        return 0

    #Sending password (succeeds if server replies with 'logged in', fails otherwise)
    print("\nSending Password...\n")
    message = password
    sckt.send(message)
    data = sckt.recv(18)
    if (data!= 'logged in'):
        print(data)
        sckt.close()
        return 0

    sckt.close()
    return 0

main()
