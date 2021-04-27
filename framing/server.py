import socket, sys, re, os
import workerThread
sys.path.append("../lib")
import params
import threading

switchesVarDefaults = (
        (('-l', '--listenPort') ,'listenPort', 50001),
        (('-?', '--usage'), "usage", False), 
        )

progname = "fileTransferServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''                                        

if paramMap['usage']:
        params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)
os.chdir("./receivedFiles")

while True:
    conn, addr = s.accept()                             # wait for incoming connection request
    print('Connected by', addr)
    work = workerThread.Worker(conn,addr)
    work.start()
