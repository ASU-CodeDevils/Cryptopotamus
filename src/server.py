""" Server """

import socketserver
import socket
from crypto import *


class ClientHandler(socketserver.BaseRequestHandler):
    state = 0
    private_key = None
    public_key = None
    asy = AsyPotamus
    crypto = Potamus

    def send(self, message):
        print("Sending: ", message, " to ", self.client_address)
        self.request.send(message)

    def die(self):
        print("Killing Handler")
        self.request.close()

    def handle(self):
        run = True
        self.asy = AsyPotamus()  # TODO: Move this to an appropriate location
        print(self.client_address)
        while run:
            data = self.request.recv(1024)
            if not data: break
            print("Received: ", data, " from ", self.client_address)  # MARKER
            run = self.parse(data)
        self.die()

    def parse(self, data):
        if self.state == 0:
            if data == b'HelloClient':
                self.state = 1
                self.send(b'HelloServer')
                self.send(self.asy.serialized_cert())
                return True
            else:
                self.die()
                return False
        elif self.state == 1:
            key = self.asy.private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                                                  algorithm=hashes.SHA1(),
                                                                  label=None))
            self.crypto = Potamus(key)
            self.state = 2
            return True


class Server(socketserver.ThreadingTCPServer):
    myHost = ''
    myPort = 50007

    def __init__(self):
        self.address_family = socket.AF_INET6
        crypto = AsyPotamus()
        addr = (self.myHost, self.myPort)
        super(Server, self).__init__(addr, ClientHandler)


if __name__ == "__main__":
    server = Server()
    server.serve_forever()
