import socket
import os
import signal
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def signal_handler(sig, frame):
    global sock
    sock.close()
    print("\nClosing abruptly")
    sys.exit(0)

def receive_file(user, sock, no_files, path):
    for i in range(int(no_files)):
        data = sock.recv(1024)
        print(data.decode())
        data = data.decode().split()
        name = data[0]
        size = data[1]
        bytesReceived = 0
        size = int(size)
        f = open(name, 'wb')
        data = sock.recv(1024)
        f.write(data)
        bytesReceived += len(data)
        print("Bytes Received so far: ", bytesReceived, "and Expected Size: ", size)
        while (bytesReceived < size):
            data = sock.recv(1024)
            f.write(data)
            bytesReceived += len(data)
            print("Bytes Received so far: ", bytesReceived, "and Expected Size: ", size)
        f.close()
        path2 = os.path.join(path, name)
        os.rename(name, path2)

def main():
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 58017
    Message = "Got it".encode()

    global sock
    signal.signal(signal.SIGINT, signal_handler)

    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    print("Connection Address: ", addr)

    user = conn.recv(1024).decode()
    print("New user: ", user)
    if not os.path.isdir(str(user)):
        os.makedirs(user)
    conn.send("User created".encode())

    data = conn.recv(1024).decode()
    data = data.split()
    if len(data) > 2:
        name = data[0]
        for i in range(len(data) - 1):
            if (i == 0):
                continue
            name = name + ' ' + data[i]
    else:
        name = data[0]
    print("The folder ", name, " will be received, containing ", data[len(data) - 1], " files")
    os.makedirs(name)
    path = os.path.join(user, name)
    os.rename(name, path)
    conn.send(Message)

    receive_file(user, conn, data[len(data) - 1], path)
    conn.close()
    
main()
