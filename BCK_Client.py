import socket
import os
import time
import signal

def send_file(folder, filename, sock):
    path = os.path.join(folder, filename)
    size = os.path.getsize(path)
    Message = filename + ' ' + str(size)
    sock.send(Message.encode())
    time.sleep(0.1)
    f = open(path, 'rb')
    bytesToSend = f.read(1024)
    while(bytesToSend):
        sock.send(bytesToSend)
        time.sleep(0.1)
        bytesToSend = f.read(1024)
    f.close()

def main():
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 58017

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect((TCP_IP, TCP_PORT))

    user = input("User: ")
    sock.send(user.encode())
    Message = sock.recv(1024)
    print("Server: ", Message.decode())

    name = input("Which folder do you want to send?\n")
    files = os.listdir(name)
    num = len(files)
    #Message = str(os.path.getsize(name))
    Message = name + ' ' + str(num)
    sock.send(Message.encode())
    sock.recv(1024)

    for i in range(num):
        send_file(name, files[i], sock)
    sock.close()

main()
