""" Server """

import socketserver
import socket
import re
from crypto import *
from helper import State
from cryptography.hazmat.primitives.asymmetric import padding


class ClientHandler(socketserver.BaseRequestHandler):
    state = 0
    sym = Potamus
    asy = AsyPotamus

    def __init__(self, request, client_address, server):
        self.asy = AsyPotamus()
        super().__init__(request, client_address, server)

    def send(self, message):
        print("Sending: ", message, " to ", self.client_address)
        self.request.send(message)

    def die(self):
        print("Killing Handler")
        self.request.close()

    def handle(self):
        run = True
        print(self.client_address)
        while run:
            data = self.request.recv(1024)
            if not data:
                break
            print("Received: ", data, " from ", self.client_address)  # MARKER
            run = self.parse(data)
        self.die()

    def parse(self, data):
        if self.state == State.NOT_CONNECTED:
            if data == b'HelloClient':
                self.state = State.NEGOTIATING
                self.send(b'HelloServer')
                self.send(self.asy.serialized_cert())
                return True
            else:
                self.die()
                return False
        elif self.state == State.NEGOTIATING:
            self.state = State.CONNECTED
            key = self.asy.private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                                                  algorithm=hashes.SHA1(),
                                                                  label=None))
            self.sym = Potamus(key)
            return True
        elif self.state == State.CONNECTED:
            plaintext = self.sym.decrypt(data)
            instruction = str
            if not plaintext.endswith(b'\x03') or not plaintext.startswith(b'\x01'):  # Message in Multiple Chunks
                pass  # TODO: multichunks logic here
            else:  # plaintext is whole message
                data_string = bytes.decode(plaintext)[1:-1]
                instruction = re.split('[\x02\x1f]', data_string)
            if instruction[0] == "login":
                login_success = self.server.validate_login(user=instruction[1], pwd=instruction[2])
                if login_success:
                    self.send(b'LoginSuccess')
                else:
                    self.send(b'LoginFailure')
            return True


class Server(socketserver.ThreadingTCPServer):
    srvhost = ''
    srvport = 49374

    def __init__(self):
        self.address_family = socket.AF_INET6
        addr = (self.srvhost, self.srvport)
        super(Server, self).__init__(addr, ClientHandler)

    def log(self, message):
        print(message)
        return message

    def validate_login(self, user, pwd):
        # TODO: write this
        if user == "test" and pwd == "pass":
            return True
        else:
            return False


if __name__ == "__main__":
    server = Server()
    server.serve_forever()
