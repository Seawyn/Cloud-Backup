#Computers' Networks Project
#Group 17

#BACKUP SERVER

import socket
import sys
import os

def child(BSport):
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_address = (socket.gethostbyname('lab6p4'), BSport)
    scktUDP.bind(udp_server_address)
    cenas = "+BS: ola jorge\n"
    #scktUDP.sendto(cenas.encode(), (socket.gethostbyname(socket.gethostname()), BSport))
    scktUDP.sendto(cenas.encode(), (socket.gethostbyname('lab6p4'), BSport))
    msg = scktUDP.recvfrom(1024)
    while msg:
        print(msg.decode())
        print('\nA new child ',  os.getpid())
    scktUDP.close()
    os._exit(0)


#chamar a funçao child quando for necessario criar novo processo
def main():
    scktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users = {}
    if(len(sys.argv) == 4 and (isinstance(sys.argv[1], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58018
        BSport = 59000
    tcp_server_address = ('localhost', CSport)
    scktTCP.bind(tcp_server_address)
    scktTCP.listen(1)
    while True:
        connection, client_address = scktTCP.accept()
        newpid = os.fork()
        if newpid == 0:
            child(BSport)
        else:
            pids = (os.getpid(), newpid)
            print("parent: %d, child: %d\n" % pids)
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
