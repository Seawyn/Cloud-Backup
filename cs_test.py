#Computers' Networks Project
#Group 17

#CENTRAL SERVER

import socket
import sys


def main():
    users = {}
    if(len(sys.argv) == 3 and (isinstance(sys.argv[2], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_address = (socket.gethostbyname('lab6p4'), CSport)
    scktUDP.bind(udp_server_address)
    a = "RGR OK\n"
    #scktUDP.sendto(a.encode() , (socket.gethostbyname(socket.gethostname()), BSport))
    while True:
        msg = scktUDP.recvfrom(1024)
        if msg:
            print(msg.decode())
        else:
            break
    scktUDP.sendto(a.encode() , ('lab6p9', BSport))
    scktUDP.close()
    return 0


main()
