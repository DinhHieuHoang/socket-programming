import json
import socket
import threading

from helper.auth_helper import *
from database.database import *

from constants import *

class Server:

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[INFO] Socket created')
        self.socket.bind((host, port))
        self.socket.listen(NUM_HOSTS)
        print('[INFO] Listening on %s:%d' % (host, port))

        self.isAlive = True
        self.clients = {}
        self.thread = None

    def start_server(self):
        self.thread = threading.Thread(name='Server thread', target=self.worker)
        self.thread.start()

    def stop_server(self):
        try:
            self.thread.join()
        except:
            print('[ERRO] Stopping server failed!')

    def worker(self):
        while server.isAlive:
            server.listening()

    def listening(self):
        try:
            socket, address = self.socket.accept()
            handshake(socket, address)
        except:
            print('[ERRO] Handshaking failed!')

    def handshake(self, socket, address):
        print('[INFO] Connection from: ', address)

        # start thread
        try:
            authen = Authenticator(socket, address)
            authen.start_thread()
        except:
            print('[ERRO] Authentication failed!')
    
    def is_alive(self):
        return self.isAlive

    def close(self):
        self.isAlive = False

        try:
            print('[INFO] Shutting down ...')
            self.socket.close()
            # DATABASE.getInstance().detach_clients()
        except:
            print('[ERRO] Shut down progess failed!')


if __name__ == '__main__':
    # Connect database

    # server 
    server = Server(SERVER_NAME, SERVER_PORT)
    server.start_server()
    print('[INFO] Server started successfully!')


    DATABASE().connect_database()
    print('[INFO] DATABASE loaded successfully!')
