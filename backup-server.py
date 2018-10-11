#Computers' Networks Project
#Group 17

#BACKUP SERVER

import socket
import sys
import os

def child(CSport, BSport):
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDP_IP = 'localhost'
    scktUDP.bind((UDP_IP, BSport))
    IP = socket.gethostbyname(socket.gethostname())
    msg = "REG " + IP  + " " + str(BSport)
    scktUDP.sendto(msg.encode(), (UDP_IP, CSport))
    n = 0
    while True:
        data, addr = scktUDP.recvfrom(1024) # buffer size is 1024 bytes
        data = data.decode()
        data = data.split()
        if data[0] == "RGR" and data[1] == "OK" and n == 0:
            n += 1
        elif data[0] == "LSU":
            usersfile = open("BS_userslist.txt", 'r')
            userslist = usersfile.readlines()
            for i in range(len(userslist)):
                if(userslist[i] == data[1] + ' ' + data[2] + '\n'):
                    print("User: " + data[1])
                    luser = data[1]
                    msg = "LUR NOK\n"
            usersfile.close()
            if(msg != "LUR NOK\n"):
                usersfile = open("BS_userslist.txt", 'a')
                usersfile.write(data[1] + ' ' + data[2] + '\n')
                usersfile.close()
                print('New user: ' + data[1])
                msg = "LUR OK\n"
                scktUDP.sendto(msg.encode(), (UDP_IP, CSport))

    os._exit(0)


def main():
    users = {}
    if(len(sys.argv) == 4 and (isinstance(sys.argv[1], int))):
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
        tcp_server_address = ('localhost', BSport)
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
                        if(data[0] == "AUT"):
                            usersfile = open("BS_userslist.txt", 'r')
                            userslist = usersfile.readlines()
                            for i in range(len(userslist)):
                                if(userslist[i] == data[1] + ' ' + data[2] + '\n'):
                                    print("User: " + data[1])
                                    luser = data[1]
                                    message = "AUR OK\n"
                                else:
                                    message = "AUR NOK\n"
                            usersfile.close()
                        elif(data[0] == "UPL"):
                            print("data: " + str(data))
                            for i in range(int(data[2])): #resolver ciclo
                                fileslist = connection.recv(1024)
                                fileslist = fileslist.decode()
                                if i == 0:
                                    print(data[1] + ': ' + fileslist + ' Bytes received')
                                else:
                                    print(fileslist + ' Bytes received')
                            message = "UPR OK\n"
                        connection.sendall(message.encode())
                    else:
                        break
            finally:
                connection.close()

    return 0


main()
