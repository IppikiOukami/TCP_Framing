import sys, re, time
from socket import *

sSocket = socket(AF_INET, SOCK_STREAM)
sSocket.bind(('127.0.0.1',50000))
sSocket.listen(100)

cSocket, addr = sSocket.accept()
time.sleep(10)
print('Connecting to {}'.format(addr))
msg = cSocket.recv(1024)

print('Message: ', msg.decode())

remoteFile = open('inServer.txt','w+')
remoteFile.write(msg.decode());
remoteFile.close()
