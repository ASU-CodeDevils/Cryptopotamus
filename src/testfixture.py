import crypto
import pickle
import server
import client

certwriter = crypto.AsyPotamus()
certwriter.write_key_and_cert("../helper/cert.pem", "../helper/key.pem")