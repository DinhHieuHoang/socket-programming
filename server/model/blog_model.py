import json

class BlogObject:
    def __init__(self, json=None, author=None, content=None, date=None):
        if json is not None:
            self.author = json['author']
            self.content = json['content']
            self.date = json['date']

        elif author is not None:
            self.author = author
            self.content = content
            self.date = date

    
    def exportJson(self):
        return json.dumps({'author': self.author, 'content': self.content, 'date': self.date})

    # Getters
    @property
    def author(self):
        return self.__author

    @property
    def content(self):
        return self.__content

    @property
    def date(self):
        return self.__date

    # Setters
    @author.setter
    def author(self, value):
        self.__author = value

    @content.setter
    def content(self, value):
        self.__content = value

    @date.setter
    def date(self, value):
        self.__date = value
