import crypto
import pickle
import server
import client

server = server.Server()
server.serve_forever()

client.Client()