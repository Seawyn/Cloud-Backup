#Computers' Networks Project
#Group 17

#CENTRAL SERVER

import socket
import sys
import os

def child(CSport, BSport):
    UDP_IP = 'localhost'
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    scktUDP.bind((UDP_IP, CSport))
    print("vou receber mensagem:")
    dataUDP, addrUDP = scktUDP.recvfrom(1024) # the problem is here
    print (dataUDP.decode())
    while True:
        a = "RGR OK\n"
        scktUDP.sendto(a.encode(), (UDP_IP, BSport))
    os._exit(0)

def main():
    users = {}
    if(len(sys.argv) == 3 and (isinstance(sys.argv[2], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000
    newpid = os.fork()
    if newpid == 0:
        child(CSport, BSport)
    else:
        scktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server_address = ('localhost', CSport)
        scktTCP.bind(tcp_server_address)
        scktTCP.listen(1)
        while True:
            connection, client_address = scktTCP.accept()
            try:
                while True:
                    data = connection.recv(1024)
                    data = data.decode()
                    data = data.split()
                    if data:
                        if(data[1] not in users):
                            users[data[1]] = data[2]
                            message = "AUR NEW\n"
                            print("New user: " + data[1])
                        else:
                            if(users[data[1]] == data[2]):
                                print("User: " + data[1])
                                message = "AUR OK\n"
                            else:
                                message = "AUR NOK\n"
                        connection.sendall(message.encode())
                    else:
                        break
            finally:
                connection.close()

    return 0


main()
