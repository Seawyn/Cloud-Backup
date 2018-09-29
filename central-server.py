#Computers' Networks Project
#Group 17

#CENTRAL SERVER

import socket
import sys

def main():
    scktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    users = {}
    if(len(sys.argv) == 3 and (isinstance(sys.argv[2], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000
        tcp_server_adress = ('localhost', CSport)
        udp_server_adress = ('localhost', BSport)
    scktTCP.bind(tcp_server_adress)
    scktUDP.bind(udp_server_adress)
    scktTCP.listen(1)
    while True:
        connection, client_adress = scktTCP.accept()
        msg = scktUDP.recvfrom(1024)
        print(msg)
        try:
            while True:
                data = connection.recv(1024)
                data = data.decode()
                data = data.split()
                scktUDP.sendto("RGR OK" , BSport)
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
