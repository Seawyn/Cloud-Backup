import socket
import os
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

main()
