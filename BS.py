#Computers' Networks Project
#Group 17

import socket
import sys

def main():
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    users = []
    BSport = 59000
    CSname = socket.gethostname()
    CSport = 58017
    if(len(sys.argv) > 1):
        for i in range(len(sys.argv)):
            if (sys.argv[i] == "-b"):
                BSport = sys.argv[i + 1]
            elif (sys.argv[i] == "-n"):
                CSname = sys.argv[i + 1]
            elif (sys.argv[i] == "-p"):
                CSport = sys.argv[i + 1]
    
