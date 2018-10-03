import socket
import sys

#chamar a funçao child quando for necessario criar novo processo
def main():
    UDP_IP = 'localhost'
    UDP_PORT = 58017
    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    users = {}
    if(len(sys.argv) == 4 and (isinstance(sys.argv[1], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000

    scktUDP.bind((UDP_IP, UDP_PORT))


    while True:
        data, addr = scktUDP.recvfrom(1024) # buffer size is 1024 bytes
        print (data.decode())
    return 0


main()
