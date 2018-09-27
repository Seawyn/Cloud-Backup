#Computers' Networks Project
#Group 17

import socket
import sys

def main():

    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if(len(sys.argv) == 4):
        CSname = input("CS name: ")
        CSport = input("Port: ")
    elif(len(sys.argv) == 3 and isinstance(sys.argv[2], str)):
        CSname = input("CS name: ")
    elif(len(sys.argv) == 3 and isinstance(sys.argv[2], int)):
        CSport = input("port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
    server_adress = ('localhost', CSport)
    user = input()
    lusername = ""
    lpass = ""
    if (isinstance(user, str)):
        log = user.split()
        if(log[0] == "login" and isinstance(log[1], str) and isinstance(log[2], str)):
            lusername = log[1]
            lpass = log[2]
            sckt.connect(server_adress)
            try:
                message = "AUT "+ lusername + " " + lpass
                sckt.sendall(message.encode())
                amount_received = 0
                amount_expected = 1024
                while amount_received == 0:
                    data = sckt.recv(1024)
                    amount_received += len(data.decode())
                    if("AUR NEW" == data.decode()):
                        success = "User " + lusername + " created"
                    elif("AUR OK" == data.decode()):
                        success = "Successful login"
                    elif("AUR NOK" == data.decode()):
                        success = "Wrong Password"
                    print(success)
            finally:
                sckt.close()
        elif(log[0] == "exit"):
            print("Successful Exit")
            return 0
    return 0

main()
