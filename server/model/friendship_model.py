import json


class FriendshipObject:
    def __init__(self, client, target):
        self.client = client
        self.target = target


    def exportJson(self):
        return json.dumps({'client': self.client, 'target': self.target})

    @property
    def client(self):
        return self.__client

    @property
    def target(self):
        return self.__target

    @client.setter
    def client(self, value):
        self.__client = value

    @target.setter
    def target(self, value):
        self.__target = value