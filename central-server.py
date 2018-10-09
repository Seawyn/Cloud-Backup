#Computers' Networks Project
#Group 17
#ps aux para obter a lista de processos
#kill -9 PID para acabar o processo
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
    dataUDP = dataUDP.decode()
    dataUDP = dataUDP.split()
    BSmsg = "+BS: " + dataUDP[1]  + " " + dataUDP[2]
    print (BSmsg)
    while True:
        a = "RGR OK\n"
        scktUDP.sendto(a.encode(), (UDP_IP, BSport))
    os._exit(0)

def main():
    users = {}
    luser = -1
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
                        if (data[0] == "DLU"):
                            if(luser != -1):
                                del users[luser]
                                luser = -1
                                message = "DLU OK\n"
                        elif(data[1] not in users):
                            users[data[1]] = data[2]
                            message = "AUR NEW\n"
                            print("New user: " + data[1])
                        elif(data[0] == "BCK"):
                            print("BCK " + luser + " [nome diretoria] [IP] " + CSport)
                        else:
                            if(users[data[1]] == data[2]):
                                print("User: " + data[1])
                                luser = data[1]
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
