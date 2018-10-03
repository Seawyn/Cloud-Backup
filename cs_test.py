#Computers' Networks Project
#Group 17

#CENTRAL SERVER

import socket
import sys


def main():
    UDP_IP = 'localhost'

    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

    return 0


main()
