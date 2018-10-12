#Computers' Networks Project
#Group 17

#BACKUP SERVER

import socket
import sys
import os
import signal
import time

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
        elif(data[0] == "LSF"):
            path = os.path.join(data[1], data[2])
            n_files = os.listdir(path)
            message = 'LFD ' + str(len(n_files)) + '\n'
            for i in range(len(n_files)):
                path2 = os.path.join(path, n_files[i])
                size = os.path.getsize(path2)
                stat = time.gmtime(os.path.getmtime(path2))
                date = time.strftime('%d.%m.%y', stat)
                file_time = time.strftime('%H:%M:%S', stat)
                message += n_files[i] + ' ' + date + ' ' + file_time + ' ' + str(size) + '\n'
            scktUDP.sendto(message.encode(), (UDP_IP, CSport))
    os._exit(0)

def send_file(luser, folder, filename, sckt_aux):
    path = os.path.join(luser, folder)
    path = os.path.join(path, filename)
    size = os.path.getsize(path)
    Message = filename + ' ' + str(size) + ' '
    sckt_aux.send(Message.encode())
    time.sleep(0.7)
    f = open(path, 'rb')
    bytesToSend = f.read(1024)
    while(bytesToSend):
        sckt_aux.send(bytesToSend)
        time.sleep(0.7)
        bytesToSend = f.read(1024)
    f.close()

def receive_file(user, sckt_aux, n_files, path):
    for i in range(int(n_files)):
        data = sckt_aux.recv(1024)
        data = data.decode().split()
        name = data[0]
        size = data[3]
        bytesReceived = 0
        size = int(size)
        f = open(name, 'wb')
        data = sckt_aux.recv(1024)
        f.write(data)
        bytesReceived += len(data)
        while (bytesReceived < size):
            data = sckt_aux.recv(1024)
            f.write(data)
            bytesReceived += len(data)
        f.close()
        path2 = os.path.join(path, name)
        os.rename(name, path2)


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
                                    if not os.path.isdir(str(data[1])):
                                        os.makedirs(data[1])
                                else:
                                    message = "AUR NOK\n"
                            usersfile.close()
                        elif(data[0] == "UPL"):
                            os.makedirs(data[1])
                            path = os.path.join(luser, data[1])
                            os.rename(data[1], path)
                            receive_file(luser, connection, data[2], path)
                            filelist = os.listdir(path)
                            totalfileslist = data[1] + ': '
                            for i in range(int(data[2])):
                                path2 = os.path.join(path, filelist[i])
                                size = os.path.getsize(path2)
                                if i == 0:
                                    totalfileslist += filelist[i] + ' ' + str(size) + ' Bytes received\n'
                                else:
                                    totalfileslist += filelist[i] + ' ' + str(size) + ' Bytes received\n'
                            message = "UPR OK\n"
                        elif(data[0] == "RSB"):
                            path = os.path.join(luser, data[1])
                            files = os.listdir(path)
                            num = len(files)
                            message = "RBR " + str(num) + '\n'
                            connection.sendall(message.encode())
                            message = ''
                            send_txt = 'Sending ' + data[1] + ': '
                            for i in range(num):
                                path2 = os.path.join(path, files[i])
                                stat = time.gmtime(os.path.getmtime(path2))
                                date = time.strftime('%d.%m.%y', stat)
                                file_time = time.strftime('%H:%M:%S', stat)
                                size = os.path.getsize(path2)
                                if(i != num-1 ):
                                    send_txt += files[i] + ', '
                                else:
                                    send_txt += files[i] + '\n'
                                message += files[i] + ' ' + date + ' ' + file_time + ' ' + str(size) + '\n'
                                time.sleep(0.7)
                                send_file(luser, data[1], files[i], connection)
                            print(send_txt)

                        connection.sendall(message.encode())
                    else:
                        break
            finally:
                connection.close()

    return 0


main()
