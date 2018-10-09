#Computers' Networks Project
#Group 17

#port=58011 user=99999 pass=zzzzzzzz '192.168.1.1'

import socket
import sys
import os
import time

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
luser = -1
lpassword = -1

def login(user, password, server_address):
    lusername = user
    lpass = password
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Resolve o bad file descriptor
    sckt.connect(server_address)
    try:
        message = "AUT "+ lusername + " " + lpass
        sckt.sendall(message.encode())
        amount_received = 0
        amount_expected = 1024
        while amount_received == 0:
            data = sckt.recv(1024)
            amount_received += len(data.decode())
            if("AUR NEW\n" == data.decode()):
                result = "User " + lusername + " created\n"
            elif("AUR OK\n" == data.decode()):
                result = "Successful login\n"
            elif("AUR NOK\n" == data.decode()):
                result = "Wrong Password\n"
            print(result)
    finally:
        sckt.close()
    return 0

def deluser(lusername, lpass, server_address):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Resolve o bad file descriptor
    sckt.connect(server_address)
    global luser
    try:
        message = "AUT "+ lusername + " " + str(lpass)
        sckt.sendall(message.encode())
        amount_received = 0
        amount_expected = 1024
        data = sckt.recv(1024)
        if("AUR OK\n" == data.decode()):
            message = "DLU\n"
            sckt.sendall(message.encode())
        result = sckt.recv(1024)
        result = result.decode()
        if(result == "DLU OK\n"):
        	luser = -1
        	print(luser)
        print(result)
    finally:
        sckt.close()
    return 0

def backupDir(user, password, server_address, dir):
    sckt.connect(server_address)
    try:
        message = "AUT " + user + " " + password
        sckt.sendall(message.encode())
        data = sckt.recv(1024)
        if ("AUR OK\n" == data.decode()):
            Message = "BCK " + dir + ' ' + str(len(os.listdir(dir)))
            sckt.sendall(Message.encode())
            #Part where he receives the ip address and port
            received = sckt.recv(1024)
            received.split()

        '''amount_received = 0
        amount_expected = 1024
        while amount_received == 0:
            data = sckt.recv(1024)
            amount_received += len(data.decode())
            if("AUR OK\n" == data.decode()):
                result = "\n"
            elif("BCK RC NUMERO QUE N ENTENDO\n" == data.decode()):
                result = "backup to: endereço port\n"
            elif("UPR OK\n" == data.decode()):
                result = "completed - RC: NOME DOS FICHEIROS"
            print(result)'''
    finally:
        sckt.close()
    return 0

def main():
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
    server_address = ('localhost', CSport)
    global luser
    while True:
        menu_input = input()
        if (isinstance(menu_input, str)):
        #FAZER CHECK NA PASSWORD
            instruction = menu_input.split()
            if(instruction[0] == "login" and isinstance(instruction[1], str) and isinstance(instruction[2], str)):
                luser = instruction[1]
                lpassword = instruction[2]
                login(luser, lpassword, server_address)
            elif(instruction[0] == "deluser"):
            		if(luser == -1):
            			print("Login required.")
            		else:
                		deluser(luser, lpassword, server_address)
            elif(instruction[0] == "backup" and instruction[1] == "dir"):
                backupDir(luser, lpassword, server_address, instruction[1])
            elif(instruction[0] == "exit"):
                return 0
            else:
                print("Error: Menu instruction invalid.\n")

    return 0

main()
