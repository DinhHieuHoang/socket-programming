import socket
import threading
import pickle

from constants import *
from model.client_model import *
from model.message_model import *
from model.client_socket_model import *

from client_helper import *

from database.database import *

class Authenticator:
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.thread = None

    def start_thread(self):
        # TODO: RUn thread here
        self.thread = threading.Thread(name='%s' % self.address[0], target=self.worker)
        self.thread.start()

    def stop_thread(self):
        self.thread.join()

    def listening(self):
        message = pickle.loads(self.socket.recv(2048))
        # print(message)

        return message

    def worker(self):
        try:
            while True:
                message = self.listening()
                if message is None:
                    self.exit()
                    break
                
                ACTION = message['action']
                if ACTION == ACTION_LOGIN:
                    if self.logIn(message):
                        print('[INFO] Logged In')

                elif ACTION == ACTION_SIGNUP:
                    if self.signUp(message):
                        print('[INFO] Signed Up')

                else:
                    print('[INFO] Log In required!')
                    self.requireLogIn(message)
                    

        except:
            print("[ERRO] Authentication failed!")

    def logIn(self, message):
        # Get client user from database using username
        client = DATABASE().get_client(message.src)

        if client is not None:
            # User existed
            print ('[INFO] Username connected: %s' % client.username)

            if message.body == client.password:
                print('[INFO] Connection from: %s:%d' % (self.address[0], self.address[1]))

                # ACCEPT MESSAGE
                msg = MessageObject(json=None,
                                    src=SERVER_NAME,
                                    dest=client.username,
                                    action=ACTION_LOGIN,
                                    body=STATUS_OK)
                # msg = MessageObject(json=None,
                #                     SERVER_NAME,
                #                     client.username,
                #                     ACTION_LOGIN,
                #                     STATUS_OK)
                self.socket.send(pickle.dumps(msg))

                # New helper thread
                clientHelper = ClientHelper(client,
                                            ClientSocketObject(client.username, client.socket),
                                            self.address)

                # TODO: Start client thread
                clientHelper.start()
                
                return True
            
            else:
                # Wrong password
                print('[INFO] Connection denied from: %s:%d' % (self.address[0], self.address[1]))

                # BAD PASS MESSAGE
                msg = MessageObject(json=None,
                                    src=SERVER_NAME,
                                    dest=message.src,
                                    action=ACTION_LOGIN,
                                    body=STATUS_BADPASS)

                self.socket.send(pickle.dumps(msg))

        else:
            # No user found in database
            # reply with unregister user message

            print('[INFO] User unregistered: %s' % message.src)

            msg = MessageObject(json=None,
                                src=SERVER_NAME,
                                dest=message.src,
                                action=ACTION_LOGIN,
                                body=STATUS_UNREGISTER)

            self.socket.send(pickle.dumps(msg))

        return False



    def signUp(self, message):
        client = ClientObject(json=message)

        if DATABASE().get_client(client.username) is None:
            # New user
            DATABASE().add_client(client)
            # create log in message
            msg = MessageObject(json=None,
                                src=client.username, 
                                dest=SERVER_NAME, 
                                action=ACTION_LOGIN, 
                                body=client.password)

            return self.logIn(msg)
        else:
            # Existing user
            msg = MessageObject(json=None,
                                src=SERVER_NAME,
                                dest=message.src,
                                action=ACTION_LOGIN,
                                body=EXISTED_USERNAME)
            self.requireLogIn(message)
            
        return False

    def requireLogIn(self, message):
        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=message.src,
                            action=ACTION_LOGIN,
                            body=ACTION_LOGIN_REQUIRED)

        self.socket.send(pickle.dumps(msg))

    def exit(self):
        print('[INFO] Exitting connection from: %s:%d' % (self.address[0], self.address[1]))
