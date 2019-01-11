from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from constants import HOST, PORT, BUF_SIZE
from gui import LoginScreen, SignUpScreen, MainScreen
from message import TYPE, DATA, RESPONSE, decode_msg

CHAT_SUFFIX = ' - chat'

class Client:
    def __init__(self):
        self.conn = socket(AF_INET, SOCK_STREAM)
        self.conn.connect((HOST, PORT))

        self.thread_receive = Thread(target=self.receive, args=(self.conn,))
        self.thread_receive.setDaemon(True)
        self.thread_receive.start()

        self.ui_active = None

    def start(self):
        self.ui_active = LoginScreen(self)
        self.ui_active.open()

    def ui_to(self, screen):
        self.ui_active = screen
        self.ui_active.open()

    def send(self, msg):
        self.conn.sendall(msg)

    def receive(self, conn):
        while True:
            recv_msg = conn.recv(BUF_SIZE)

            if recv_msg is not None:
                recv_msg = decode_msg(recv_msg)
                msg_type = recv_msg[TYPE]
                data = recv_msg[DATA]

                if msg_type == RESPONSE.LOGIN_SUCCESS:
                    self.ui_active.wd.queueFunction(self.ui_active.to_main)

                elif msg_type == RESPONSE.LOGIN_FAIL:
                    self.ui_active.inform_login_failed()   

                elif msg_type == RESPONSE.SIGNUP_SUCCESS:
                    self.ui_active.inform_signup_succeeded()
                    self.ui_active.wd.queueFunction(self.ui_active.to_main)

                elif msg_type == RESPONSE.SIGNUP_FAIL:
                    self.ui_active.inform_signup_failed()

                elif msg_type == RESPONSE.INIT:
                    self.ui_active.receive_init_info(data[0], data[1], data[2], data[3], data[4], data[5])

                elif msg_type == RESPONSE.CHATS:
                    self.ui_active.confirm_chat(data[0], data[1], data[2])

                elif msg_type == RESPONSE.CHAT:
                    # self.ui_active.receive_chat(data[0], data[1], data[2])
                    try:
                        self.ui_active.receive_chat(data[0], data[1], data[2])
                    except:
                        receiver = data[0] + CHAT_SUFFIX
                        self.ui_active.chat(receiver)

                elif msg_type == RESPONSE.PROFILE:
                    self.ui_active.receive_profile(data[0], data[1], data[2], data[3])

                elif msg_type == RESPONSE.BLOGS:
                    self.ui_active.receive_blogs(data)

                elif msg_type == RESPONSE.CONFIRM_FRIEND:
                    self.ui_active.ask_confirm_friend(data)

                elif msg_type == RESPONSE.FRIEND:
                    self.ui_active.receive_friend_request_reply(data[0], data[1], data[2], data[3])