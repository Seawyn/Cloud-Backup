#Computers' Networks Project
#Group 17

#CENTRAL SERVER

import socket
import sys
import os

scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def child():
    data, addr = scktUDP.recvfrom(1024) # the problem is here
    print(data)
    if data:
        print (data.decode())
    else:
        os._exit(0)

def main():
    UDP_IP = 'localhost'

    users = {}
    if(len(sys.argv) == 3 and (isinstance(sys.argv[2], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000
    a = "RGR OK\n"

    scktUDP.sendto(a.encode(), (UDP_IP, 58017))
    '''if os.fork() == 0:
        child()
        print("child process.")
    else:
        print("entrei no else")'''
    print("vou receber")
    data, addr = scktUDP.recvfrom(1024) # the problem is here
    print("recebi")
    if data:
        print (data.decode())


    return 0


main()
