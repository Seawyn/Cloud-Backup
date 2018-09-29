#Computers' Networks Project
#Group 17

import socket
import sys

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def login(user, password, server_adress):
    lusername = user
    lpass = password
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
                result = "User " + lusername + " created"
            elif("AUR OK" == data.decode()):
                result = "Successful login"
            elif("AUR NOK" == data.decode()):
                result = "Wrong Password"
            print(result)
    finally:
        sckt.close()
    return 0

def deluser(user):
    return 0
'''def backupDir():
def restoreDir():
def dirList():
def filelistDir():
def deleteDir():
def logout():'''
def exit():
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
    server_adress = ('localhost', CSport)
    menu_input = input()
    '''menu = {"login": login(), "deluser": deluser(), "backup dir": backupDir(), "restore dir": restoreDir(),
    "dirlist": dirList(), "filelist dir": filelistDir(), "delete dir": deleteDir(), "logout": logout(), "exit": exit()}'''
    if (isinstance(menu_input, str)):
        instruction = menu_input.split()
        #FAZER CHECK NA PASSWORD
        if(instruction[0] == "login" and isinstance(instruction[1], str) and isinstance(instruction[2], str)):
            login(instruction[1], instruction[2], server_adress)
        elif(instruction[0] == "deluser"):
            print("not done yet")
        elif(instruction[0] == "exit"):
            exit()
    return 0

main()
