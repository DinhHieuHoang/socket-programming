import json
import socket
from authenticator import *
from constants import *

class Server:

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[INFO] Socket created')
        self.socket.bind((host, port))
        # self.socket.listen(num_host)
        print('[INFO] Listening on %s:%d' % (host, port))

        self.isAlive = True
        self.clients = {}

    def listening(self):
        try:
            socket, address = self.socket.accept()
            handshake(socket, address)
        except:
            print('[ERRO] Handshaking failed!')

    def handshake(self, socket, address):
        print('[INFO] Connection from: ', address)

        # start thread
        authen = Authenticator(socket, address)


