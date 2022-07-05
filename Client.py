'''
Simple Client
Run in command window with: Client.py <host address> <port>
'''

import socket
import sys
from time import sleep

s = socket.socket()
try:      
    if sys.argv[1:]:
        try:
            host = sys.argv[1]# ip of raspberry pi
            port = int(sys.argv[2])
        except (IndexError, ValueError):
            print("Invalid Entry.")
            sys.exit()
    else:
        print("Please input argument IP for the server")
        sys.exit()     
except TimeoutError:
    print("Server not available")

try:
    s.connect((host, port))
    print(s.recv(1024))
except (ConnectionRefusedError, socket.gaierror, TimeoutError):
    print("Server not available")
    sys.exit()

while(True):
    try:
        try:
            print(s.recv(1024).decode())
            if (s.recv(1024).decode() == ''):
                print("Connection with server has been lost")
                s.close()
                sys.exit()
            sleep(0.5)
        except OSError:
            print("Connection with server has been lost")
            s.close()
            sys.exit()
    except KeyboardInterrupt:
        print("Closing connection...")
        s.close()
        sys.exit()
