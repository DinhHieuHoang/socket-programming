import json

class ClientObject:

    def __init__(self, json=None, username=None, password=None, dob=None, avatar=None):
        if json is not None:
            self.username = json['username']
            self.password = json['password']
            self.dob = json['dob']
            self.avatar = json['avatar']
        elif username is not None:
            self.username = username
            self.password = password
            self.dob = dob
            self.avatar = avatar

    # Export json object
    def exportJson(self):
        return json.dumps({'username': self.username, 'password': self.password, 'dob': self.dob, 'avatar': self.avatar})

    # Getters
    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def dob(self):
        return self.__dob

    @property
    def avatar(self):
        return self.__avatar

    # Setters
    @username.setter
    def username(self, value):
        self.__username = value

    @password.setter
    def password(self, value):
        self.__password = value

    @dob.setter
    def dob(self, value):
        self.__dob = value

    @avatar.setter
    def avatar(self, value):
        self.__avatar = value

    