import socket
import sys

#chamar a funçao child quando for necessario criar novo processo
def main():
    users = {}
    if(len(sys.argv) == 4 and (isinstance(sys.argv[1], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
        BSport = 59000

    scktUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_address = (socket.gethostbyname('lab6p4'), CSport)
    #scktUDP.bind(udp_server_address)
    cenas = "+BS: ola jorge\n"
    #scktUDP.sendto(cenas.encode(), (socket.gethostbyname(socket.gethostname()), BSport))
    scktUDP.sendto(cenas.encode(), (socket.gethostbyname('lab6p4'), CSport))
    while True:
        msg = scktUDP.recvfrom(1024)
        if msg:
            print(msg.decode())
        else:
            break
    scktUDP.close()

    return 0


main()
