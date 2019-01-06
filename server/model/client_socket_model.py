import socket

class ClientSocketObject:
    def __init__(self, username=None, socket=None):
        self.username = username
        self.socket = socket

    # Getters
    @property
    def username(self):
        return self.username

    @property
    def socket(self):
        return self.socket

    # Setters
    @username.setter
    def username(self, value):
        self.username = value

    @socket.setter
    def socket(self, value):
        self.socket = value
