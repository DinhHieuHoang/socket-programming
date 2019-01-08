import json

class MessageObject:
    def __init__(self, json=None, src=None, dest=None, action=None, body=None):
        if json is not None:
            self.src = json['src']
            self.dest = json['dest']
            self.action = json['action']
            self.body = json['body']
        elif src is not None:
            self.src = src
            self.dest = dest
            self.action = action
            self.body = body

    # Create JSON object of message
    def exportJson(self):
        return json.dumps({'src': self.src, 'dest': self.dest, 'action': self.action, 'body': self.body})

    # Getters
    @property
    def src(self):
        return self.__src

    @property
    def dest(self):
        return self.__dest

    @property
    def action(self):
        return self.__action

    @property
    def body(self):
        return self.__body

    # Setters
    @dest.setter
    def dest(self, value):
        self.__dest = value
    
    @src.setter
    def src(self, value):
        self.__src = value
    
    @action.setter
    def action(self, value):
        self.__action = value
    
    @body.setter
    def body(self, value):
        self.__body = value

    
    