'''Test fixture GUI for client'''

from tkinter import *
from tkinter import messagebox


class MessageFrame(Frame):
    ownerClient = None
    text_message = None

    def __init__(self, master, client):
        Frame.__init__(self, master)
        self.master = master
        self.ownerClient = client
        self.init_window()

    def init_window(self):
        self.master.title("Cryptopotamus")
        self.pack(fill=BOTH, expand=1)
        self.text_message = Text(self, height=3)
        self.text_message.pack()
        button_send = Button(self, text="Send", command=self.client_send)
        button_send.pack()
        button_quit = Button(self, text="Quit", command=self.client_exit)
        button_quit.pack()

    def client_exit(self):
        self.ownerClient.quit()

    def client_send(self):
        self.ownerClient.send(self.text_message.get("1.0", "end-1c"))

    def showcipher(self, ciphertext):
        messagebox.showinfo("Ciphertext", ciphertext)


class LoginFrame(Frame):
    ownerClient = None

    def __init__(self, master, client):
        super().__init__(master)
        self.ownerClient = client

        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")

        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")

        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command = self.login_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def login_clicked(self):
        username = self.entry_1.get()
        password = self.entry_2.get()

        #print(username, password)

        self.ownerClient.login(username, password)
        self.master.destroy()