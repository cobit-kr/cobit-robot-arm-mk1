from socket import *
import time 

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8082))

while True:
    msg = "siva\r\n"
    clientSock.send(msg)
    rx_msg = clientSock.recv(1024)
    time.sleep(1)