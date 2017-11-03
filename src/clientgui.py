from tkinter import *


class MessageWindow(Frame):
    ownerClient = None
    message = None

    def __init__(self, master=None, client=None):
        Frame.__init__(self, master)
        self.master = master
        self.ownerClient = client
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        text_message = Text(self, height=3, textvariable=self.message)
        text_message.pack()
        button_send = Button(self, text="Send", command=self.client_send)
        button_send.pack()
        button_quit = Button(self, text="Quit", command=self.client_exit)
        button_quit.pack()

    def client_exit(self):
        self.ownerClient.quit()

    def client_send(self):
        self.ownerClient.send(self.message)