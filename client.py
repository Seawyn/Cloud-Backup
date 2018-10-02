#Computers' Networks Project
#Group 17

#port=58011 user=99999 pass=zzzzzzzz '192.168.1.1'

import socket
import sys

sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def login(user, password, server_address):
    lusername = user
    lpass = password
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

def deluser(user):
    return 0
'''def backupDir():
def restoreDir():
def dirList():
def filelistDir():
def deleteDir():
def logout():'''


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
    while True:
        menu_input = input()
        '''menu = {"login": login(), "deluser": deluser(), "backup dir": backupDir(), "restore dir": restoreDir(),
        "dirlist": dirList(), "filelist dir": filelistDir(), "delete dir": deleteDir(), "logout": logout(), "exit": exit()}'''
        if (isinstance(menu_input, str)):
        #FAZER CHECK NA PASSWORD
            instruction = menu_input.split()
            if(instruction[0] == "login" and isinstance(instruction[1], str) and isinstance(instruction[2], str)):
                login(instruction[1], instruction[2], server_address)
            elif(instruction[0] == "deluser"):
                print("not done yet")
            elif(instruction[0] == "exit"):
                return 0
            else:
                print("Error: Menu instruction invalid.\n")

    return 0

main()
