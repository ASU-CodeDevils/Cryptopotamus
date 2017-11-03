'''Chat client'''

import sys
import socket
import select

from clientgui import *
from crypto import *

class Client:
    def quit(self):
        exit()


    def send(self, message):
        bytecode = str.encode(message)


    def main(self):
        root = Tk()
        root.geometry("400x150")
        app = MessageWindow(root, self)
        root.mainloop()


if __name__ == "__main__":
    Client().main()