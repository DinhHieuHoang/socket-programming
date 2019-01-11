from json import dumps, loads

TYPE = 'type'
DATA = 'data'

def make_msg(msg_type, data=None):
    return dumps({TYPE: msg_type, DATA: data}).encode('utf-8')

def decode_msg(msg):
    return loads(msg.decode('utf-8'))

class REQUEST:
    LOGIN = 'login'
    SIGNUP = 'signup'
    GET_CHATS = 'get chats'
    GET_INIT_INFO = 'get init'
    CHAT = 'chat'
    CHANGE_AVATAR = 'change avatar'
    GET_PROFILE = 'get profile'
    POST_BLOG = 'post blog'
    SHARE_BLOG = 'share blog'
    ADD_FRIEND = 'add friend'
    CONFIRM_FRIEND = 'confirm friend'

class RESPONSE:
    LOGIN_SUCCESS = 'login success'
    LOGIN_FAIL = 'login fail'
    SIGNUP_SUCCESS = 'signup success'
    SIGNUP_FAIL = 'signup fail'
    INIT = 'init'
    CHATS = 'chats'
    CHAT = 'chat'
    PROFILE = 'profile'
    BLOGS = 'blogs'
    CONFIRM_FRIEND = 'confirm friend'
    FRIEND = 'friend'