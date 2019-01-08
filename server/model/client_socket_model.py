import socket

class ClientSocketObject:
    def __init__(self, username=None, socket=None):
        self.username = username
        self.socket = socket

    # Getters
    @property
    def username(self):
        return self.__username

    @property
    def socket(self):
        return self.__socket

    # Setters
    @username.setter
    def username(self, value):
        self.__username = value

    @socket.setter
    def socket(self, value):
        self.__socket = value
