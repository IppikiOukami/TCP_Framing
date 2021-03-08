import socket, sys, re, params

pack_size = 1024

def fill_buffer():
    try:
        out = open("bio.txt",'rb')
    except IOError:
        print('Unable to open bio.txt')
        return

    packs = []
    while True:
        data = out.read(pack_size)
        if not data:
            break
        packs.append(data)
    return packs

program = "ftp_server"

packs = fill_buffer()

inPort = 50009
inAddr = '127.0.0.1'

sock  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((inPort, inAddr))
sock.listen(1)

conn, addr = sock.accept()

print(f"Connected on : {addr}")

while packs:
    print(packs[0])
    data = packs[0]
    if not data:
        print("Nothing to read, Nothing to send, terminating...")
        break
    conn.send(data)
    packs = packs[1:]
print("File Transfer Complete")
conn.shutdown(socket.SHIT_WR)
conn.close()
