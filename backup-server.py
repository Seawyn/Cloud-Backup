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
        #command = data.split()
        if data == "RGR OK\n" and n == 0:
            n += 1
        #elif command[0] == "LSU":

    os._exit(0)


def main():
    #scktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users = {}
    if(len(sys.argv) == 4 and (isinstance(sys.argv[1], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000
    #tcp_server_address = ('localhost', CSport)
    #scktTCP.bind(tcp_server_address)
    #scktTCP.listen(1)
    newpid = os.fork()
    if newpid == 0:
        child(CSport, BSport)
    #while True:
        #connection, client_address = scktTCP.accept()
        """else:
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
                connection.close()"""

    return 0


main()
