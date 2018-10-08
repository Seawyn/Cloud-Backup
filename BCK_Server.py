import socket
import os
<<<<<<< HEAD
import time

def send_file(folder, filename, sock):
   path = os.path.join(folder, filename)
   stat = time.gmtime(os.path.getmtime(path))
   time1 = time.strftime('%d.%m.%y', stat)
   time2 = time.strftime('%H:%M:%S', stat)
   size = os.path.getsize(path)
   Message = filename + ' ' + time1 + ' ' + time2 + ' ' + str(size)
   sock.send(Message.encode())
   f = open(path, 'rb')
   bytesToSend = f.read(1024)
   while(bytesToSend):
       sock.send(bytesToSend)
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
   Message = str(num)
   sock.send(Message.encode())
   sock.recv(1024)

   for i in range(num):
       send_file(name, files[i], sock)
       data = sock.recv(1024)
       print(data.decode())
   sock.close()

=======

def receive_file(user, sock, no_files):
    for i in range(int(no_files)):
        data = sock.recv(1024)
        print(data.decode())
        data = data.decode().split()
        name = data[0]
        time1 = data[1]
        time2 = data[2]
        size = data[3]
        bytesReceived = 0
        size = int(size)
        f = open(name, 'wb')
        data = sock.recv(1024)
        f.write(data)
        bytesReceived += len(data.decode())
        #print("Bytes Received so far: ", bytesReceived, "and Expected Size: ", size)
        while (bytesReceived < size):
            data = sock.recv(1024)
            f.write(data)
            bytesReceived += len(data.decode())
            #print("Bytes Received so far: ", bytesReceived, "and Expected Size: ", size)
        Message = "Finished"
        sock.send(Message.encode())
        path = os.path.join(user, name)
        os.rename(name, path)
        f.close()

def main():
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 58017
    Message = "Got it".encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    print("Connection Address: ", addr)

    user = conn.recv(1024).decode()
    if not os.path.isdir(str(user)):
        print("New user: ", user)
        os.makedirs(user)
    else:
        print("User already exists, folder was not created")
    conn.send("User created".encode())

    data = conn.recv(1024).decode()
    print(data, "files will be received")
    conn.send(Message)

    receive_file(user, conn, data)
    conn.close()
    
>>>>>>> 1b0faa3bd6f2e9c3e01bb313246b82015c145a51
main()
