""" Server """

import socketserver
import socket


class ClientHandler(socketserver.BaseRequestHandler):
    state = 0
    key = None

    def send(self, message):
        print("Sending: ", message, " to ", self.client_address)
        self.request.send(message)

    def handle(self):
        print(self.client_address)
        while True:
            data = self.request.recv(1024)
            if not data: break
            print("Received: ", data, " from ", self.client_address)    # MARKER
            self.parse(data)
        self.request.close()

    def parse(self, data):
        if self.state == 0:
            if data == b"HelloClient" :
                self.state = 1
                self.send(b"HelloServer")
            else:
                self.request.close()


class Server(socketserver.ThreadingTCPServer):
    myHost = ''  # server machine, '' means local host
    myPort = 50007  # listen on a non-reserved port number

    def __init__(self):
        self.address_family = socket.AF_INET6
        addr = (self.myHost, self.myPort)
        super(Server, self).__init__(addr, ClientHandler)


if __name__ == "__main__":
    server = Server()
    server.serve_forever()
