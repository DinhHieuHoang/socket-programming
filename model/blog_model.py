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
        return self.author

    @property
    def content(self):
        return self.content

    @property
    def date(self):
        return self.date

    # Setters
    @author.setter
    def author(self, value):
        self.author = value

    @content.setter
    def content(self, value):
        self.content = value

    @date.setter
    def date(self, value):
        self.date = value
