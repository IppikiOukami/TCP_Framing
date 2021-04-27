import socket, sys, re, time, os
import framedSocket
sys.path.append("../lib")
import params

switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-d', '--delay'), 'delay', "0"),
        (('-?', '--usage'), "usage", False), # boolean (set if present)
        )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)
server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()
    
try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)
    
s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break
                                                                                    
if s is None:
    print('could not open socket')
    sys.exit(1)

framedSock = framedSocket.Framed_Socket(s)

while True:
    print("Enter File to send or QUIT to exit:")
    fileName = (os.read(0, 1024).decode()).strip()
    if fileName != 'QUIT' or fileName != None:    
        filePath = ("files/" + fileName)
        if os.path.exists(filePath):
            print("Sending %s" % fileName)
            framedSock.tx(fileName.encode())
            serverReply = framedSock.rx()
            if serverReply == "OK":
                found = open(filePath, "r")
                data = found.read()
                if not data:
                    print("empty file")
                    continue
                framedSock.tx(data.encode())
            elif serverReply == "wait":
                print("Server is busy")
            else:
                print("File previously transferred")
        else:
            print("file not found")
            continue
    else:
        print("I quit...")
        s.close()
        sys.exit(0)
