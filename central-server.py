#Computers' Networks Project
#Group 17
#ps aux para obter a lista de processos
#kill -9 PID para acabar o processo
#CENTRAL SERVER

import socket
import sys
import os

flag_BCK = 0
luser = -1
lpassword = -1

def child(CSport, BSport):
    global flag_BCK
    global luser
    global lpassword

    UDP_IP = 'localhost'
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    scktUDP.bind((UDP_IP, CSport))
    print("vou receber mensagem:")
    dataUDP, addrUDP = scktUDP.recvfrom(1024) # the problem is here
    dataUDP = dataUDP.decode()
    dataUDP = dataUDP.split()
    BSmsg = "+BS: " + dataUDP[1]  + " " + dataUDP[2]
    print (BSmsg)
    a = "RGR OK\n"
    scktUDP.sendto(a.encode(), (UDP_IP, BSport))
    while True:
        if(flag_BCK == 1):
            BSmsg = "LSU " + luser + ' ' + lpassword
            scktUDP.sendto(BSmsg.encode(), (UDP_IP, BSport))
    os._exit(0)

def main():
    users = {}
    global luser
    global lpassword
    global flag_BCK
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
                                #Falta condição para os novos users
                        elif(data[0] == "AUT" and data[1] not in users):
                            usersfile = open("userslist.txt", 'a')
                            usersfile.write(data[1] + ' ' + data[2] + '\n')
                            usersfile.close()
                            users[data[1]] = data[2]
                            message = "AUR NEW\n"
                            print("New user: " + data[1])
                        elif(data[0] == "BCK"):
                            print(data[0] +  ' ' + luser + ' ' + data[1] + ' ' + str(socket.gethostbyname(socket.gethostname())) + ' ' + str(BSport))
                            data = connection.recv(1024)
                            flag_BCK = 1
                        else:
                            usersfile = open("userslist.txt", 'r')
                            lista = usersfile.readlines()
                            for i in range(len(lista)):
                                if(lista[i] == data[1] + ' ' + data[2] + '\n'):
                                    print("User: " + data[1])
                                    luser = data[1]
                                    message = "AUR OK\n"
                            usersfile.close()
                        connection.sendall(message.encode())
                    else:
                        break
            finally:
                connection.close()

    return 0


main()
