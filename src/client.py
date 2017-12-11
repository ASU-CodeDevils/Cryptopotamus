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
        self.gui_login_window()

    def quit(self):
        exit()

    def init_sock(self):
        host = 'localhost'
        port = 49374
        baresock = socket(AF_INET6, SOCK_STREAM)
        context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile='../scache/crt.pem')
        self.servsock = context.wrap_socket(baresock, server_hostname=host)
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

    def listen_loop(self):
        while True:
            data = self.servsock.recv(1024)
            if not data:
                break
            print("Received: ", data)  # MARKER
            self.parse(data)
        self.servsock.close()

    def login(self, username, password):
        sendstr = "\x01login\x02" + username + "\x1f" + password + "\x03"
        self.servsock.send(data=str.encode(sendstr))
        print("sent")
        # TODO: Display waiting dialog or something here
        # rest of login process handled via listener

    def parse(self, data):
        pass

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


if __name__ == "__main__":
    Client()