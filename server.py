from socket import socket, AF_INET, SOCK_STREAM, error as socket_error
from threading import Thread

from constants import HOST, PORT, BUF_SIZE
from database import Database
from message import TYPE, DATA, REQUEST, RESPONSE, make_msg, decode_msg

class Server:
    def __init__(self):
        self.conn = socket(AF_INET, SOCK_STREAM)
        self.conn.bind((HOST, PORT))
        self.conn.listen()

        print('[INFO] Server started on %s:%d' % (HOST, PORT))

        self.active_users = dict()
        self.db = Database()

    def listen(self):
        while True:
            try:
                conn, addr = self.conn.accept()
                thread = Thread(target=self.handle, args=(conn, addr))
                thread.setDaemon(True)
                thread.start()

                print('[INFO] Client\'s connection established from', addr)
            except:
                print('[ERROR] Client\'s connection failed')

    def handle(self, conn, addr):
        while True:
            try:
                msg = conn.recv(BUF_SIZE)

                if msg is not None:
                    msg = decode_msg(msg)
                    msg_type = msg[TYPE]
                    data = msg[DATA]

                    if msg_type == REQUEST.LOGIN:
                        auth = self.db.authenticate(data[0], data[1])
                        if auth:
                            response = make_msg(RESPONSE.LOGIN_SUCCESS) 
                            self.active_users[data[0]] = conn
                        else:
                            response = make_msg(RESPONSE.LOGIN_FAIL)

                    elif msg_type == REQUEST.SIGNUP:
                        reg = self.db.add_user(data[0], data[1], data[2])                        
                        if reg:
                            response = make_msg(RESPONSE.SIGNUP_SUCCESS) 
                            self.active_users[data[0]] = conn
                        else:
                            response = make_msg(RESPONSE.SIGNUP_FAIL)

                    elif msg_type == REQUEST.GET_INIT_INFO:
                        friends, avatars = self.db.get_friends(data)
                        users = self.db.get_users()
                        profile = self.db.get_profile(data)
                        latest_blog = self.db.get_latest_blog(data)
                        blogs = self.db.get_blogs(data)
                        response = make_msg(RESPONSE.INIT, (users, friends, avatars, profile, latest_blog, blogs))

                    elif msg_type == REQUEST.GET_CHATS:
                        res = self.db.get_chats(data[0], data[1])
                        response = make_msg(RESPONSE.CHATS, res)

                    elif msg_type == REQUEST.CHAT:
                        self.db.add_chat(data[0], data[1], data[2])
                        response = make_msg(RESPONSE.CHAT, data)

                        if data[1] in self.active_users:
                            self.active_users[data[1]].sendall(response)
                        else:
                            pass

                    elif msg_type == REQUEST.CHANGE_AVATAR:
                        self.db.change_avatar(data[0], data[1])
                        response = None

                    elif msg_type == REQUEST.GET_PROFILE:
                        res = self.db.get_profile(data)
                        res.append(self.db.get_latest_blog(data))
                        response = make_msg(RESPONSE.PROFILE, res)

                    elif msg_type == REQUEST.POST_BLOG:
                        self.db.add_blog(data[0], (data[1], data[2]))
                        res = self.db.get_blogs(data[0])
                        print(res)
                        response = make_msg(RESPONSE.BLOGS, res)

                    elif msg_type == REQUEST.SHARE_BLOG:
                        friends, _ = self.db.get_friends(data[0])
                        for friend in friends:
                            self.db.add_blog(friend, (data[1], data[2]))

                            if friend in self.active_users:
                                self.active_users[friend].sendall(make_msg(RESPONSE.BLOGS, self.db.get_blogs(friend)))
                        response = None

                    elif msg_type == REQUEST.ADD_FRIEND:
                        if data[1] in self.active_users:
                            self.active_users[data[1]].sendall(make_msg(RESPONSE.CONFIRM_FRIEND, data))
                        response = None

                    elif msg_type == REQUEST.CONFIRM_FRIEND:
                        if data[0] in self.active_users:
                            if data[2]:
                                self.db.add_friend(data[0], data[1])
                            avatar = self.db.get_profile(data[1])[2]
                            data.append(avatar)
                            self.active_users[data[0]].sendall(make_msg(RESPONSE.FRIEND, data))
                            data[-1] = self.db.get_profile(data[0])[2]
                            response = make_msg(RESPONSE.FRIEND, data)
                        
                    if response is not None:
                        conn.sendall(response)
                        response = None

            except socket_error:
                print('[INFO] Connection at', addr, 'has closed')
                for e_user, e_conn in self.active_users.items():
                    if conn == e_conn:
                        del self.active_users[e_user]
                        break 
                break