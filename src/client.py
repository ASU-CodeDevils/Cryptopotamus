'''Chat client'''

from clientgui import *
from crypto import *
from socket import *
import threading
from helper import State
from cryptography.hazmat.primitives.asymmetric import padding
import ssl


class Client(object):
    sym = Potamus
    servsock = socket
    loginstatus = 0
    recvbuffer = b''
    cert = x509.Certificate
    symkey = None
    connected = False

    def __init__(self):
        threading.Thread(target=self.init_sock).start()
        self.init_crypt()
        self.gui_login_window()

    def quit(self):
        exit()

    def init_sock(self):
        host = 'localhost'
        port = 49374
        baresock = socket(AF_INET6, SOCK_STREAM)
        context = ssl.create_default_context()
        self.servsock = context.wrap_socket(baresock, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2, verify=False)
        try:
            self.servsock.connect((host, port))
            print("Connection Successful")  # MARKER
        except ConnectionRefusedError:
            print("Connection Refused")  # MARKER
            return
        except InterruptedError:
            print("Connection Interrupted")  # MARKER
            return
        threading.Thread(target=self.listen_loop).start()
        self.handshake()  # Move this?

    def listen_loop(self):
        while True:
            data = self.servsock.recv(1024)
            if not data:
                break
            print("Received: ", data)  # MARKER
            self.parse(data)
        self.servsock.close()

    def login(self, username, password):
        self.secure_send(data="\x01login\x02" + username + "\x1f" + password + "\x03")
        # TODO: Display waiting dialog or something here
        # rest of login process handled via listener

    def parse(self, data):
        if self.loginstatus == State.NOT_CONNECTED:
            if data == b'HelloServer':
                self.loginstatus = State.NEGOTIATING
        elif self.loginstatus == State.NEGOTIATING:
            self.recvbuffer += data
            if self.recvbuffer[-26:] == b"-----END CERTIFICATE-----\n":
                if self.validate_cert():
                    ciphertext = self.cert.public_key().encrypt(self.symkey,
                                                                padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                                                             algorithm=hashes.SHA1(),
                                                                             label=None))
                    self.servsock.sendall(ciphertext)
                    self.loginstatus = State.CONNECTED
                    self.recvbuffer = b''
                else:
                    print("Could Not Validate Certificate")
        elif self.loginstatus == State.CONNECTED:
            if data == b'LoginSuccess':
                print("Login Successful!")
                self.gui_message_window()
            elif data == b'LoginFailure':
                print("Login Failed")

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
        self.sym = Potamus(self.symkey)

    def handshake(self):
        self.servsock.sendall(b'HelloClient')

    def secure_send(self, data):
        if isinstance(data, str):
            bytecode = str.encode(data)
        ciphertext = self.sym.encrypt(bytecode)
        self.servsock.sendall(ciphertext)


if __name__ == "__main__":
    Client()
