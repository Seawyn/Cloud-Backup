#Computers' Networks Project
#Group 17

#BACKUP SERVER

import socket
import sys
import os

def child():
    print('\nA new child ',  os.getpid())
    os._exit(0)

def parent():
    newpid = os.fork()
    if newpid == 0:
        child()
    else:
        pids = (os.getpid(), newpid)
        print("parent: %d, child: %d\n" % pids)
     reply = input("q for quit / c for new fork")
     if reply == 'c':
         continue
     else:
         break


#chamar a funçao child quando for necessario criar novo processo
def main():
    scktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    users = {}
    if(len(sys.argv) == 4 and (isinstance(sys.argv[1], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58018
        BSport = 59000
    tcp_server_adress = ('localhost', CSport)
    udp_server_adress = ('localhost', BSport)
    scktTCP.bind(tcp_server_adress)
    scktUDP.bind(udp_server_adress)
    scktTCP.listen(1)
    cenas = "+BS: "
    scktUDP.sendto(cenas.encode(), (socket.gethostbyname(socket.gethostname()), BSport))
    #scktUDP.sendto(cenas.encode(), ('194.210.229.184', BSport))
    while True:
        connection, client_adress = scktTCP.accept()
        msg = scktUDP.recvfrom(1024)
        print(msg.decode())
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
