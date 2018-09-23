#Computers' Networks Project
#Group 17

import socket
import sys

def main():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Accounts = []
    recv_counter = 0                    #Dictates whether an id (0) or a password (1) will be received
    if(len(sys.argv) == 3 and (isinstance(sys.argv[2], int))):
        CSport = input("Port: ")
    elif(len(sys.argv) == 3):
        raise TypeError('Error: invalid input.')
    else:
        CSport = 58017
    server_adress = ('localhost', CSport)
    sckt.bind(server_adress)
    sckt.listen(1)
    while True:
        connection, client_adress = sckt.accept()
        try:
            while True:
                data = connection.recv(16)
                print(data)

                #verification of id attribute
                if (recv_counter == 0):
                    if (not(isinstance(data, char)) and int(data) < 100000):
                        data = 'Invalid User\n'
                        print(data)
                        conn.send(data)
                        break
                    else:
                        ind = data
                        data = 'accepted'       #Variable that allows the main app to keep sending information
                        print(data)
                        recv_counter++

                #verification of password attribute
                #TODO: Restrict the Password verification (it still accepts characters like '.' and '-')
                elif (recv_counter == 1):
                    for i in range(0, len(data)):
                        if not(isinstance(data[i], int) or isinstance(data[i], str)):
                            data = 'Invalid Password'
                            print(data)
                            conn.send(data)
                            break
                        else
                            pswd = data
                            data = 'logged in'
                            print(data)
                            recv_counter++

                else:
                    #For now, the accounts database will consist of a list of tuples
                    tp_assist = (ind, pswd)
                    Accounts.append(tp_assist)
                    break
        finally:
            connection.close()
    return 0


main()
