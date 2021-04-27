import socket, sys, re, os
import framedSocket
sys.path.append("../lib")
import params
import threading
from threading import Thread

threadNum = 0
lock = threading.Lock()
fileSet = set()

class Worker(Thread):
    def __init__(self,conn,addr):
        global threadNum
        Thread.__init__(self, name = "Thread-%d" % threadNum)
        threadNum += 1
        self.conn = conn
        self.addr = addr

    def checkTransfer(self, fileName):
        global fileSet
        global lock
        lock.acquire()

        if fileName in fileSet:
            inUse = False
        else:
            inUse = True
            fileSet.add(fileName)
        lock.release()
        return inUse
        
    def start(self):
        framedSock = framedSocket.Framed_Socket(self.conn)
        fileName = framedSock.rx()
        filePath = "receivedFiles/" + fileName
        inUse = checkTransfer(fileName)
        if not inUse:
            framedSock.tx(b'wait')
        elif os.path.exists(filePath):
            fs.tx(b'No')
        else:
            framedSock.tx(b'OK')
            try:
                fileData = framedSock.rx()
                print("Writing file contents")
                fd = os.open(fileName, os.O_CREAT | os.O_WRONGLY)
                os.write(fd, fileData.encode())
                os.close(fd)

            except:
                framedSock.tx(b'Error writting file')
        self.conn.shutdown(socket.SHUT_WR)

    def end(self,fileName):
        global fileSet
        fileSet.remove(fileName)
