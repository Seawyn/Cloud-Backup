#Computers' Networks Project
#Group 17
#ps aux para obter a lista de processos
#kill -9 PID para acabar o processo
#CENTRAL SERVER

#Otherwise, the CS exchanges LSF-LFD messages with the BS, to
#receive the list of missing or changed files in the backup.

import socket
import sys
import os
import signal
from multiprocessing import Process, Pipe


scktTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def signal_handler(sig, frame):
    scktTCP.close()
    scktUDP.close()
    sys.exit(0)

def child(CSport, BSport, childPipe):
    UDP_IP = 'localhost'
    signal.signal(signal.SIGINT, signal_handler)
    scktUDP.bind((UDP_IP, CSport))
    dataUDP, addrUDP = scktUDP.recvfrom(1024)
    dataUDP = dataUDP.decode()
    dataUDP = dataUDP.split()
    BSmsg = "+BS: " + dataUDP[1]  + " " + dataUDP[2]
    print (BSmsg)
    msg = "RGR OK\n"
    scktUDP.sendto(msg.encode(), (UDP_IP, BSport))
    luser = childPipe.recv()
    lpassword = childPipe.recv()
    while True:
        if childPipe.recv() == 1:
            BSmsg = "LSU " + str(luser) + ' ' + str(lpassword)
            scktUDP.sendto(BSmsg.encode(), (UDP_IP, BSport))
            dataUDP, addr = scktUDP.recvfrom(1024) #the problem is here
            if(dataUDP.decode() == "LUR OK\n" or dataUDP.decode() == "LUR NOK\n"):
                childPipe.send(2)
                #p.join()
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
    parentPipe, childPipe = Pipe()
    newpid = os.fork()
    if newpid == 0:
        p = Process(target=child, args=(CSport, BSport, childPipe))
        p.start()
    else:
        signal.signal(signal.SIGINT, signal_handler)
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
                            parentPipe.send(data[1])
                            parentPipe.send(data[2])
                            message = "AUR NEW\n"
                            print("New user: " + data[1])
                        elif(data[0] == "BCK"):
                            print(data[0] +  ' ' + luser + ' ' + data[1] + ' ' + str(socket.gethostbyname(socket.gethostname())) + ' ' + str(BSport))
                            num = data[2]
                            CSusersfiles = open("backup_list.txt", 'r')
                            userslist = CSusersfiles.readlines()
                            found_user = 0
                            for i in range(len(userslist)):
                                if(userslist[i] == luser + ' ' + data[1]):
                                    found_user = 1
                            if not found_user:
                                CSusersfiles.close()
                                CSusersfiles = open("backup_list.txt", 'a')
                                CSusersfiles.write(luser + ' ' + data[1] + '\n')
                                CSusersfiles.close()

                            parentPipe.send(1)
                            data = connection.recv(1024)
                            while True:
                                if parentPipe.recv() == 2:
                                    message = "BKR " + ' ' + str(socket.gethostbyname(socket.gethostname())) + ' ' + str(BSport) + ' ' + str(num)
                                    connection.sendall(message.encode())
                                    message = data.decode()
                                    break
                        elif data[0] == "LSD":
                            print("List request")
                            CSusersfiles = open("backup_list.txt", 'r')
                            n_dir = CSusersfiles.readlines()
                            fnum = 0
                            message = ''
                            for i in range(len(n_dir)):
                                n_dir[i] = n_dir[i].split()
                                if (luser == n_dir[i][0]):
                                    fnum += 1
                                    message += ' ' + n_dir[i][1]
                            message = "LDR " + str(fnum) + message + '\n'
                            connection.sendall(message.encode())
                        #elif data[0] == "LSF":

                        else:
                            usersfile = open("userslist.txt", 'r')
                            userslist = usersfile.readlines()
                            for i in range(len(userslist)):
                                if(userslist[i] == data[1] + ' ' + data[2] + '\n'):
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
