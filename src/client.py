'''Chat client'''

from clientgui import *
from crypto import *
from socket import *


class Client:
        crypto = Potamus
        sockobj = socket

        def quit(self):
            self.sockobj.close()
            exit()

        def send(self, message):
            bytecode = str.encode(message)
            ciphertext = self.crypto.encrypt(bytecode)
            self.sockobj.send(ciphertext)

        def gui_login_window(self):
            root = Tk()
            login = LoginFrame(root, self)
            root.mainloop()

        def gui_message_window(self):
            root = Tk()
            mw = MessageFrame(root, self)

        def login(self, username, password):
            self.send(username)
            self.send(password)
            self.gui_message_window()

        def init_crypt(self):
            key = Potamus.generate_key()
            self.crypto = Potamus(key)

        def init_sockets(self):
            serverloc = 'localhost'
            port = 50007
            self.sockobj = socket(AF_INET6, SOCK_STREAM)
            self.sockobj.connect((serverloc, port))

        def main(self):
            self.init_crypt()
            self.init_sockets()
            self.gui_login_window()


if __name__ == "__main__":
    Client().main()
