""" Server """

from socket import *                    # get socket constructor and constants
myHost = ''                             # '' = all available interfaces on host
myPort = 50007                          # listen on a non-reserved port number

sockobj = socket(AF_INET6, SOCK_STREAM)       # make a TCP socket object
sockobj.bind((myHost, myPort))               # bind it to server port number
sockobj.listen(2)                            # listen, allow 5 pending connects

while True:                                  # listen until process killed
    connection, address = sockobj.accept()   # wait for next client connect
    print('Server connected by', address)    # connection is a new socket
    while True:
        data = connection.recv(1024)         # read next line on client socket
        print('Received Data:', data)
        if not data: break                   # send a reply line to the client
        connection.send(b'Echo=>' + data)    # until eof when socket closed
    connection.close()
