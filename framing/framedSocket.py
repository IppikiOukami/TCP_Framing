class Framed_Socket:
    def __init__(self, socket):
        self.connected = socket
        self.payload = ''

    def tx(self,message):
        charLength = str(len(message))
        byteLength = bytearray(charLength,'utf-8')
        message = byteLength + message
        self.connected.send(message)

    def rx(self):
        message = ''
        if not self.payload:
            self.payload += self.connected.recv(100).decode()
            start, end = splitter(self.payload)
            message += self.payload[start:end]
            self.payload = self.payload[end:]


        while self.payload:
            start, end = splitter(self.payload)
            if len(payload) < end: self.payload += self.connected.recv(100).decode()
            else:
                message += self.payload[start:end]
                self.payload = self.payload[end:]

        return message

def splitter(chunk):
    num = ''

    while chunk[0].isdigit():
        num += chunk[0]
        chunk = chunk[1:]

    if num.isnumeric():
        return len(num)+1, int(num)+(len(num)+1)
    else:
        return None
