import os
import json
import pickle
from time import gmtime, strftime

from model.client_model import *
from model.client_socket_model import *
from model.message_model import *
from model.blog_model import *

from database.database import *

from constants import *

class ClientHelper:
    def __init__(self, client, client_socket, address):
        self.client = client
        self.socket = client_socket
        self.address = address
        
        DATABASE().add_client_socket(self.socket)

    def start(self):
        # Start this object as thread
        pass

    def listening(self):
        message = pickle.loads(self.socket.recv(2048))
        # print(message)
        return message

    def handle_action(self, ACTION, message):

        # Client's basic functions
        if ACTION == ACTION_SENDMESSAGE:
            # send message to friend
            self.sendMessage(message)

        elif ACTION == ACTION_SEARCH:
            # search for friend
            self.search(message)

        elif ACTION == ACTION_ADDFRIEND:
            # add a new friend to friend list
            self.addFriend(message)

        elif ACTION == ACTION_REMOVEFRIEND:
            # remove a friend from friend list
            self.removeFriend(message)

        elif ACTION == ACTION_RETRIEVEONLINE:
            # get list of online friends
            self.retrieveOnline(message)

        elif ACTION == ACTION_GETFRIENDS:
            # return list of friends
            self.getFriends(message)

        elif ACTION == ACTION_POSTBLOG:
            # post a new blog
            self.postBlog(message)

        # Retrieve client's information: detail, blogs, avatar
        elif ACTION == ACTION_GETDETAIL:
            # get a client's detail info
            self.getDetail(message)

        elif ACTION == ACTION_GETBLOG:
            # get a client's blogs
            self.getBlog(message) 

        elif ACTION == ACTION_GETAVATAR:
            # get a client's avatar
            self.getAvatar(message)

        # Set self avatar
        elif ACTION == ACTION_SETAVATAR:
            # set current user avatar
            self.setAvatar(message)

        elif ACTION == ACTION_EXIT:
            self.exit()
            return 0

    def worker(self):
        try:
            while True:
                message = self.listening()

                if message is None:
                    self.exit()
                    break

                if self.handle_action(message['action'], message):
                    return
                
        except:
            print('[ERRO] Client handler failed for %s:%d !' % (self.address[0], self.address[1]))

    def sendMessage(self, message):
        # send message to friend
        dest_socket = DATABASE().get_socket(message.dest)

        if dest_socket is not None:
            # send "bytestring" of message
            dest_socket.send(message.exportJson())

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_SENDMESSAGE,
                            body=STATUS_OK)

        self.socket.send(pickle.dumps(msg))

    def search(self, message):
        # search for friend
        query = message['body']

        client_list = DATABASE().get_all_client()

        ret = []

        for user in client_list:
            if query in user.username:
                ret.append(user.username)

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_SEARCH,
                            body=pickle.dumps(ret))

        self.socket.send(pickle.dumps(msg))


    def addFriend(self, message):
        # add a new friend to friend list
        client = message.src
        target = message.dest

        if not DATABASE().is_friend(client, target):
            DATABASE().create_friendship(client, target)

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_ADDFRIEND,
                            body=STATUS_OK)

        self.socket.send(pickle.dumps(msg))

    def removeFriend(self, message):
        # remove a friend from friend list
        client = message.src
        target = message.dest

        if DATABASE().is_friend(client, target):
            DATABASE().remove_friendship(client, target)

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_REMOVEFRIEND,
                            body=STATUS_OK)

        self.socket.send(pickle.dumps(msg))

    def retrieveOnline(self, message):
        # get list of online friends
        currently_online = DATABASE().get_online_users()

        friends = DATABASE().get_friend_list(message.src)

        ret = []

        for user in friends:
            if user in currently_online:
                ret.append(user)

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_RETRIEVEONLINE,
                            body=pickle.dumps(ret))

        self.socket.send(pickle.dumps(msg))

    def getFriends(self, message):
        # return list of friends
        friends = DATABASE().get_friend_list()

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_GETFRIENDS,
                            body=pickle.dumps(friends))

        self.socket.send(pickle.dumps(msg))

    def postBlog(self, message):
        # post a new blog
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        blog = BlogObject(json=None,
                            author=message.src,
                            content=message.body,
                            date=time)

        DATABASE().add_blog(blog)

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_POSTBLOG,
                            body=STATUS_OK)

        self.socket.send(pickle.dumps(msg))

    def getDetail(self, message):
        # get a client's detail info
        client = DATABASE().get_client(message.body)

        if client is not None:
            msg = MessageObject(json=None,
                                src=SERVER_NAME,
                                dest=self.client.username,
                                action=ACTION_GETDETAIL,
                                body=client.exportJson())

            self.socket.send(pickle.dumps(msg))

        else:
            msg = MessageObject(json=None,
                                src=SERVER_NAME,
                                dest=self.client.username,
                                action=ACTION_GETDETAIL,
                                body=STATUS_NOTFOUND)

            self.socket.send(pickle.dumps(msg))


    def getBlog(self, message):
        # get a client's blogs
        blogs = DATABASE().get_blogs(message.body)

        msg = MessageObject(json=None,
                            src=SERVER_NAME,
                            dest=self.client.username,
                            action=ACTION_GETBLOG,
                            body=pickle.dumps(blogs))

        self.socket.send(pickle.dumps(msg))

    def getAvatar(self, message):
        # get a client's avatar
        # TODO
        pass

    def setAvatar(self, message):
        # set current user avatar
        pass

    def exit(self):
        print('[INFO] Exitting connection from: %s:%d' % (self.address[0], self.address[1]))
        DATABASE().remove_client_socket(self.client)