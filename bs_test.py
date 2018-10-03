import socket
import sys
import os

scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def child():
    msg = "+BS: "
    print("oi")
    scktUDP.sendto(msg.encode(), (UDP_IP, 58017))
    print("oiDSA")
    print("child process.")
    os._exit(0)


#chamar a funçao child quando for necessario criar novo processo
def main():
    UDP_IP = 'localhost'
    UDP_PORT = 58017
    users = {}
    if(len(sys.argv) == 4 and (isinstance(sys.argv[1], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000

    scktUDP.bind((UDP_IP, UDP_PORT))

    data, addr = scktUDP.recvfrom(1024) # buffer size is 1024 bytes
    ola = 0
    while ola < 2:
        if data:
            print (data.decode())
            data = 0
        else:
            #child()
            msg = "+BS: "
            print(addr)
            scktUDP.sendto(msg.encode(), addr)
            print("mandei msg")
        ola += 1
        '''if os.fork() == 0:
                print("oi")
                child()
            else:
                print("entrei no else")'''

    return 0


main()
