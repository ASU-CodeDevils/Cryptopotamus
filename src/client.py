'''Chat client'''

from clientgui import *
from crypto import *

class Client:
    app = None
    f = None

    def quit(self):
        exit()


    def send(self, message=None):
        bytecode = str.encode(message)
        key = Potamus.generate_key()
        f = Potamus(key)
        ciphertext = f.encrypt(bytecode)
        self.app.showcipher(ciphertext)


    def main(self):
        root = Tk()
        root.geometry("400x150")
        self.app = MessageWindow(root, self)
        root.mainloop()


if __name__ == "__main__":
    Client().main()