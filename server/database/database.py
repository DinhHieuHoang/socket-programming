from os.path import join

from tinydb import TinyDB, Query

import sys
sys.path.append('..')

from model.client_model import *
from model.blog_model import *
from model.friendship_model import *
from model.message_model import *

class _DATABASE:
    _instance = None

    def connect_database(self):
        self.clients = TinyDB(join('.', 'database', 'CLIENTS.json'))
        print('[INFO] ClientDB loaded!')

        self.blogs = TinyDB(join('.', 'database', 'BLOGS.json'))
        print('[INFO] BlogDB loaded!')

        self.friendships = TinyDB(join('.', 'database', 'FRIENDSHIPS.json'))
        print('[INFO] FriendDB loaded!')


        # List of ClientSocketObjects
        self.client_sockets = []
        

    def add_client_socket(self, client_socket_object):
        # ClientSocketObject
        self.client_sockets.append(client_socket_object)

    def remove_client_socket(self, client_socket_object):
        # ClientSocketObject
        self.client_sockets.remove(client_socket_object)

    def get_socket(self, username):
        # get user socket
        for item in self.client_sockets:
            if item.username is username:
                return item

        return None


    # ========= Clients & Friends ==========
    def get_online_users(self):
        # get list online users
        online = []

        for item in self.client_sockets:
            online.append(item.username)

        return online
        

    def get_client(self, username):
        # Get user detail
        query = Query()

        # return 1 json string of ClientObject with username
        # refer to add_client below
        tmp = self.clients.search(query.username==username)

        if len(tmp) == 0:
            return None
        
        ret = json.loads(tmp[0])
        return ClientObject(json=ret)

    def add_client(self, clientObject):
        # key: username
        # value: str(jsonObject)
        self.clients.insert({'username': clientObject.username, 'value': clientObject.exportJson()})

    def get_all_client(self):
        # Return list of clients as ClientObject
        clients_list = []

        ret = self.clients.all()

        for client in ret:
            ret.append(json.loads(client['value']))

        return clients_list

    # ========= Clients & Friends ==========




    # === Blogs ===
    def get_blogs(self, username):
        # Get blogs by username
        blogs = []
        
        q = Query()

        tmp = self.blogs.search(q.username==username)

        for item in tmp:
            blogs.append(json.loads(item['value']))

        return blogs

    def add_blog(self, blog):
        self.blogs.insert({'username':blog.author, 'value':blog.exportJson()})
    # === Blogs ===



    # === Friendships ===
    def is_friend(self, client, target):
        """
        client: username of client - str
        target: username of target - str
        """
        q = Query()

        tmp = self.friendships.search(q.username==client)

        for item in tmp:
            friendship = json.loads(item['value'])
            if (friendship.client is client) and (friendship.target is target):
                return True

        return False

    def create_friendship(self, client, target):
        """
        Input:
            str - username
        """
        tmp = FriendshipObject(client, target)
        self.friendships.insert({'username': client, 'value': tmp.exportJson()})


        tmp = FriendshipObject(target, client)
        self.friendships.insert({'username': target, 'value': tmp.exportJson()})


    def remove_friendship(self, client, target):
        q = Query()

        tmp = FriendshipObject(client, target)
        self.friendships.remove(q.value==tmp.exportJson())

        tmp = FriendshipObject(target, client)
        self.friendships.remove(q.value==tmp.exportJson())

    def get_friend_list(self, username):
        """
        Return list of friends' usernames
        """
        friends = []

        q = Query()

        ret = self.friendships.search(q.username==username)

        for item in ret:
            tmp = json.loads(item['value'])

            friends.append(tmp['target'])

        return friends

    # === Friendships ===
    



    

def DATABASE():
    if _DATABASE._instance is None:
        _DATABASE._instance = _DATABASE()
    return _DATABASE._instance

# s1 = DATABASE()
# s2 = DATABASE()

# assert s1 is s2
# s1.connect_database()