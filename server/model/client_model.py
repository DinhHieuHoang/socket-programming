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
        return self.username

    @property
    def password(self):
        return self.password

    @property
    def dob(self):
        return self.dob

    @property
    def avatar(self):
        return self.avatar

    # Setters
    @username.setter
    def username(self, value):
        self.username = value

    @password.setter
    def password(self, value):
        self.password = value

    @dob.setter
    def dob(self, value):
        self.dob = value

    @avatar.setter
    def avatar(self, value):
        self.avatar = value

    