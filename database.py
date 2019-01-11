from pickledb import load

PATH = 'server.db'
INIT = 'db init'
DEFAULT_AVATAR = 'assets/default-avatar.png'

PASS = 'pass'
DOB = 'dob'
AVATAR = 'avatar'
FRIENDS = 'friends'
CHAT = 'chat'
USERS = 'users'
BLOG = 'blog'

class Database:
    def __init__(self):
        self.db = load(PATH, True)

        if not self.db.get(INIT):
            self.db.set(USERS, [])

            admin = 'admin'
            self.add_user(admin, 'admin', 'Confidential')
            the = 'lltthe@apcs.vn'
            self.add_user(the, 'the', 'Aug 11, 1997')
            tue = 'tvdtue@apcs.vn'
            self.add_user(tue, 'tue', 'Sep 09, 1997')

            self.db.set(self.concat_key([the, FRIENDS]), [admin, tue])
            self.db.set(self.concat_key([tue, FRIENDS]), [admin, the])
            self.db.set(self.concat_key([admin, FRIENDS]), [the, tue])

            self.db.set(self.concat_key([admin, the, CHAT]), [('This is a demo chat', admin), ('This is also a demo chat', the)] * 10)
            self.db.set(self.concat_key([admin, BLOG]), [('Unknown', 'This is a demo blog'), ('Unknown', 'This is a very long demo blog. Let see how the UI can handle it')] * 5)
            
            self.db.set(INIT, True)

        print('[INFO] Database connected')

    def concat_key(self, key_list):
        return ' - '.join(key_list)

    def add_user(self, username, password, dob, avatar=DEFAULT_AVATAR):
        if not self.db.get(username):
            self.db.set(username, {PASS: password, DOB: dob, AVATAR: avatar})
            self.db.append(USERS, [username])
            return True
        return False

    def authenticate(self, username, password):
        if not self.db.get(username):
            return False
        if (self.db.get(username))[PASS] == password:
            return True
        return False

    def get_friends(self, username):
        friends = self.db.get(self.concat_key([username, FRIENDS]))
        if not friends:
            friends = []
        avatars = []
        for friend in friends:
            avatars.append(self.db.get(friend)[AVATAR])
        return (friends, avatars)

    def get_chats(self, chatter1, chatter2):
        key = self.concat_key([chatter1, chatter2, CHAT])
        chats = self.db.get(key)
        if not chats:
            key = self.concat_key([chatter2, chatter1, CHAT])
            chats = self.db.get(key)
        if not chats:
            chats = []
        return (chatter1, chatter2, chats)

    def add_chat(self, chatter1, chatter2, text):
        key = self.concat_key([chatter1, chatter2, CHAT])
        chats = self.db.get(key)
        if not chats:
            key = self.concat_key([chatter2, chatter1, CHAT])
            chats = self.db.get(key)
        if not chats:
            chats = []
        chats.append((text, chatter1))
        self.db.set(key, chats)

    def change_avatar(self, username, avatar):
        user = self.db.get(username)
        user[AVATAR] = avatar
        self.db.set(username, user)

    def get_users(self):
        return self.db.get(USERS)

    def get_profile(self, username):
        res = self.db.get(username)
        return [username, res[DOB], res[AVATAR]]

    def add_blog(self, username, blog):
        key = self.concat_key([username, BLOG])
        blogs = self.db.get(key)
        if not blogs:
            blogs = []
        if blog not in blogs:
            blogs.append(blog)  
        self.db.set(key, blogs)     

    def share_blog(self, username, blog):
        friends, _ = self.get_friends(username)

        for friend in friends:
            self.add_blog(friend, blog)

    def get_blogs(self, username):
        key = self.concat_key([username, BLOG])
        res = self.db.get(key)
        if not res:
            res = []
        return res

    def get_latest_blog(self, username):
        blogs = self.get_blogs(username)
        if len(blogs) == 0:
            return None
        return blogs[-1]

    def add_friend(self, user1, user2):
        friends1, _ = self.get_friends(user1)
        friends2, _ = self.get_friends(user2)
        friends1.append(user2)
        friends2.append(user1)
        self.db.set(self.concat_key([user1, FRIENDS]), friends1)
        self.db.set(self.concat_key([user2, FRIENDS]), friends2)