import os
import socket
import logging
import socketserver
import re
import time
import ssl

from OpenSSL import SSL, crypto

logging.basicConfig(level=logging.DEBUG,
                    format='%(relativeCreated)6d %(threadName)s %(message)s')


class ClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """
        Handle request from the client.
        :return:
        """
        logging.info("Handlin\'")
        data = self.request.recv(1024).strip()
        data_string = bytes.decode(data)[1:-1]
        logging.info("Received data: " + data_string)
        instruction = re.split('[\x02\x1f]', data_string)
        if instruction[0] == "login":
            login_success = self.server.validate_login(user=instruction[1], pwd=instruction[2])
            if login_success:
                logging.info("Client entered secure area")
                self.request.send("You entered the secure area")


class Server(socketserver.ThreadingTCPServer):
    srvhost = ''
    srvport = 49374

    def __init__(self,
                 request_handler_class=ClientHandler,
                 certfile="../scache/crt.pem",
                 keyfile="../scache/key.pem",
                 ssl_version=ssl.PROTOCOL_TLSv1_2,
                 bind_and_activate=True):
        self.address_family = socket.AF_INET6
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        server_address = (self.srvhost, self.srvport)
        super(Server, self).__init__(server_address, request_handler_class, bind_and_activate)

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        context = ssl.create_default_context()
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        context.check_hostname = False  # Solves catch-22 in ssl.py
        context.verify_mode = ssl.CERT_OPTIONAL
        logging.info("New Request from " + fromaddr[0])
        connstream = context.wrap_socket(newsocket, server_side=True)
        logging.info("Socket Wrapped")
        return connstream, fromaddr

    def validate_login(self, user, pwd):
        # TODO: write this
        if user == "test" and pwd == "pass":
            return True
        else:
            return False


if __name__ == "__main__":
    server = Server()
    server.serve_forever()
