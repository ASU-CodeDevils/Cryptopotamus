'''Chat client'''

from clientgui import *
from crypto import *
from socket import *
import threading


class Client(object):
    crypto = Potamus
    servsock = socket
    loginstatus = 0
    recvbuffer = b''
    cert = x509.Certificate
    symkey = None

    def __init__(self):
        threading.Thread(target=self.run_socks).start()
        self.init_crypt()
        self.gui_login_window()

    def run_socks(self):
        connected = self.init_sock()
        if connected:
            self.listen_loop()

    def quit(self):
        exit()

    def send(self, message):
        bytecode = str.encode(message)
        ciphertext = self.crypto.encrypt(bytecode)
        self.servsock.send(ciphertext)

    def init_sock(self):
        host = 'localhost'
        port = 50007
        self.servsock = socket(AF_INET6, SOCK_STREAM)
        try:
            self.servsock.connect((host, port))
            print("Connection Successful")  # MARKER
            return True
        except ConnectionRefusedError:
            print("Connection Refused")  # MARKER
            return False
        except InterruptedError:
            print("Connection Interrupted")  # MARKER
            return False

    def login(self, username, password):
        self.servsock.send(b'HelloClient')  # TODO: Handle exception if client can't connect

        self.gui_message_window()

    def listen_loop(self):
        while True:
            data = self.servsock.recv(1024)
            if not data: break
            print("Received: ", data)  # MARKER
            self.parse(data)  # Do some stuff
        self.servsock.close()

    def parse(self, data):
        if self.loginstatus == 0:
            if data == b'HelloServer':
                self.loginstatus = 1
        elif self.loginstatus == 1:
            self.recvbuffer += data
            str = bytes.decode(self.recvbuffer)
            if bytes.decode(self.recvbuffer)[-26:] == "-----END CERTIFICATE-----\n":
                if self.validate_cert():
                    self.loginstatus = 2
                    ciphertext = self.cert.public_key().encrypt(self.symkey,
                                                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                                                             algorithm=hashes.SHA1(),
                                                                             label=None))
                    self.servsock.send(ciphertext)
                    self.loginstatus = 2
                else:
                    print("Could Not Validate Certificate")

    def gui_login_window(self):
        root = Tk()
        login = LoginFrame(root, self)
        root.mainloop()

    def gui_message_window(self):
        root = Tk()
        mw = MessageFrame(root, self)

    def gui_alert_login_fail(self):
        pass

    def validate_cert(self):
        self.cert = x509.load_pem_x509_certificate(self.recvbuffer, default_backend())
        return True

    def init_crypt(self):
        self.symkey = Potamus.generate_key()
        self.crypto = Potamus(self.symkey)


# class State(IntEnum):    NOT_CONNECTED = 1


if __name__ == "__main__":
    Client()
