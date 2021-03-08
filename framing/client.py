import sys, re, time
from socket import *

localFile, host, remoteFile = None, None, None

if len(sys.argv) > 1:
    localFile = sys.argv[1]
    host, remoteFile = sys.argv[2].split(':')
else:
    print("Verify proper command call: missing args")
    sys.exit(1)
    
sPort = 50000

cSocket = socket(AF_INET, SOCK_STREAM)
cSocket.connect((host,sPort))

packets = []

txt = open(localFile, 'rb')

while True:
    data = txt.read(10)
    if not data: break
    packets.append(data)
txt.close()
while packets:
    cSocket.send(packets[0])
    packets = packets[1:]
print("Transfer Complete!")
cSocket.close()
    
