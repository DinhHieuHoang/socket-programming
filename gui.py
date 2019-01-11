from appJar import gui
from re import match
from datetime import date, datetime
from uuid import uuid4

from constants import APP_NAME
from message import make_msg, REQUEST

TITLE = 'title'
USERNAME = 'Username'
PASSWORD = 'Password'
SUBMIT = 'Submit'

class LoginScreen:
    def __init__(self, client):
        self.client = client

        self.wd = gui(APP_NAME + ' - Login Screen', '480x260', showIcon=False)
        self.wd.setIcon('assets/icon-login.png')

        self.wd.addLabel(TITLE, 'Welcome to ' + APP_NAME)

        self.wd.startLabelFrame('Login', sticky='ew')        
        self.wd.setPadding(0, 10)

        self.wd.addLabelEntry(USERNAME)
        self.wd.setEntryDefault(USERNAME, 'Enter your email')
        #self.wd.setFocus(USERNAME)

        self.wd.addLabelSecretEntry(PASSWORD)

        self.wd.addButtons([SUBMIT, 'Cancel'], [self.submit, self.close])
        self.wd.stopLabelFrame()

        self.wd.addLabel('Not having an account yet?')
        self.wd.addButton('Sign Up', self.signup)

        self.wd.enableEnter(self.submit)

    def open(self):
        self.wd.go()

    def close(self):
        self.wd.stop()

    def submit(self):
        data = (self.wd.getEntry(USERNAME), self.wd.getEntry(PASSWORD))
        self.client.send(make_msg(REQUEST.LOGIN, data))

    def signup(self):
        self.close()
        self.client.ui_to(SignUpScreen(self.client))

    def to_main(self):
        self.close()
        self.client.ui_to(MainScreen(self.client, self.wd.getEntry(USERNAME)))

    def inform_login_failed(self):
        self.wd.errorBox('Login Failed', 'Invalid account!\nPlease check your username and password and try again!')

REPASSWORD = 'Confirm Password'
DOB = 'dob'

class SignUpScreen:
    def __init__(self, client):
        self.client = client

        self.wd = gui(APP_NAME + ' - Sign Up Screen', showIcon=False)
        self.wd.setIcon('assets/icon-register.png')

        self.wd.addLabel(TITLE, 'Welcome to ' + APP_NAME)

        self.wd.startLabelFrame('Sign Up', sticky='ew')        
        self.wd.setPadding(0, 10)

        self.valid_username = False
        self.wd.addLabelValidationEntry(USERNAME, colspan=2)
        self.wd.setEntryDefault(USERNAME, 'Must be an email')
        self.wd.setEntryWaitingValidation(USERNAME)
        self.wd.setEntryChangeFunction(USERNAME, self.validate_username)

        self.valid_password = False
        self.password = ''
        self.wd.addLabelValidationEntry(PASSWORD, colspan=2)
        self.wd.setEntryWaitingValidation(PASSWORD)
        self.wd.setEntryChangeFunction(PASSWORD, self.validate_password)

        self.repassword = ''
        self.wd.addLabelValidationEntry(REPASSWORD, colspan=2)
        self.wd.setEntryWaitingValidation(REPASSWORD)
        self.wd.setEntryChangeFunction(REPASSWORD, self.validate_repassword)

        self.wd.addLabel('Date of birth:', row=4, column=0)
        self.wd.addDatePicker(DOB, row=4, column=1)
        current_year = date.today().year
        self.wd.setDatePickerRange(DOB, current_year-50, current_year-11)
        self.wd.setDatePicker(DOB, date(1990, 1, 1))

        self.wd.addButtons([SUBMIT, 'Cancel'], [self.submit, self.close], colspan=2)
        self.wd.disableButton(SUBMIT)
        self.wd.stopLabelFrame()

        self.wd.addLabel('Already having an account?')
        self.wd.addButton('Login', self.login)

        self.wd.enableEnter(self.submit)

    def open(self):
        self.wd.go()

    def close(self):
        self.wd.stop()

    def toggleSubmitButton(self):
        if self.valid_username and self.valid_password:
            self.wd.enableButton(SUBMIT)
        else:
            self.wd.disableButton(SUBMIT)

    def validate_username(self):
        self.valid_username = False
        inp = self.wd.getEntry(USERNAME)
        if inp == '':
            self.wd.setEntryWaitingValidation(USERNAME)
        elif match(r'[\w\.-]+@[\w-]+(\.\w+)+', inp):
            self.wd.setEntryValid(USERNAME)
            self.valid_username = True
        else:
            self.wd.setEntryInvalid(USERNAME)

        self.toggleSubmitButton()        

    def validate_password(self):
        self.valid_password = False
        inp = self.wd.getEntry(PASSWORD)
        if inp == '':
            self.wd.setEntryWaitingValidation(PASSWORD)
            self.password = ''
        else:
            self.wd.setEntryValid(PASSWORD)
            n = len(inp)
            self.wd.setEntry(PASSWORD, '*' * n)
            if n > len(self.password):
                self.password += inp[-1]
            else:
                self.password = self.password[:n]

            if self.repassword == '':
                self.wd.setEntryWaitingValidation(REPASSWORD)
            elif self.repassword == self.password:
                self.wd.setEntryValid(REPASSWORD)
                self.valid_password = True
            else:
                self.wd.setEntryInvalid(REPASSWORD)

        self.toggleSubmitButton()

    def validate_repassword(self):
        self.valid_password = False
        inp = self.wd.getEntry(REPASSWORD)
        if inp == '':
            self.wd.setEntryWaitingValidation(REPASSWORD)
            self.repassword = ''
        else:
            n = len(inp)
            self.wd.setEntry(REPASSWORD, '*' * n)
            if n > len(self.repassword):
                self.repassword += inp[-1]
            else:
                self.repassword = self.repassword[:n]

            if self.repassword == self.password:
                self.wd.setEntryValid(REPASSWORD)
                self.valid_password = True
            else:
                self.wd.setEntryInvalid(REPASSWORD)
        
        self.toggleSubmitButton()

    def submit(self):
        dob = self.wd.getDatePicker(DOB).strftime('%b %d, %Y')
        data = (self.wd.getEntry(USERNAME), self.password, dob)
        self.client.send(make_msg(REQUEST.SIGNUP, data))

    def inform_signup_failed(self):
        self.wd.errorBox('Sign Up Failed', 'The current email has been used!\nPlease try a new email!')

    def inform_signup_succeeded(self):
        self.wd.infoBox('Sign Up Succeeded', 'Your account has been created successfully!\nOn closing this pop-up you will be logged in automatically!')

    def login(self):
        self.close()
        self.client.ui_to(LoginScreen(self.client))

    def to_main(self):
        self.close()
        self.client.ui_to(MainScreen(self.client, self.wd.getEntry(USERNAME)))

FRIENDS = 'Friends'
HOME = 'Home'
FEATURES = 'Features'
BLOG = 'Blog'
PROFILE_VIEWER = 'Profile Viewer'

AVATAR = 'Avatar'
HOME_EMAIL = 'for-demo-an-email-only@sample.com'
HOME_NOTE = 'Home Note'
SEARCH = 'Search user by email'
VIEW_PROFILE = 'View Profile'

CHAT_SUFFIX = ' - chat'
VIEW_PROFILE_SUFFIX = ' - view_profile'
INP_SUFFIX = ' - inp'

PROFILE_AVATAR = 'profile avatar'
PROFILE_USERNAME = 'profile username'
PROFILE_DOB = 'profile dob'
PROFILE_ADD_FRIEND = 'profile add friend'
PROFILE_BLOG = 'profile blog'

BLOG_INP = BLOG + INP_SUFFIX
POST = 'Post'

class MainScreen:
    def __init__(self, client, user):
        self.client = client
        self.user = user

        self.wd = gui(APP_NAME, '920x690', showIcon=False)
        self.wd.setIcon('assets/icon-user.png')

        self.wd.startLabelFrame(HOME, row=0, column=0, rowspan=1, colspan=3)

        dummy = 'DummyLabel'
        self.wd.addLabel(dummy, row=0, column=0)
        self.wd.removeLabel(dummy)
        
        self.wd.addImage(AVATAR, 'assets/default-avatar.png', row=0, column=1, rowspan=6)
        self.wd.setImageSize(AVATAR, 100, 100)
        self.wd.setImageSubmitFunction(AVATAR, self.change_avatar)
        self.wd.setImageCursor(AVATAR, 'hand2')
        self.wd.setImageTooltip(AVATAR, 'Change avatar')

        self.wd.addLabel(HOME_EMAIL, self.user, row=1, column=2)
        self.wd.setLabelSubmitFunction(HOME_EMAIL, self.view_profile)
        self.wd.setLabelCursor(HOME_EMAIL, 'hand2')
        self.wd.setLabelTooltip(HOME_EMAIL, 'View own profile')
        
        for i in range(3, 20):
            self.wd.addLabel(dummy, row=0, column=i)
            self.wd.removeLabel(dummy)

        self.wd.addLabel(HOME_NOTE, 'Click the avatar to change; Click the email to show your profile', row=2, column=2)
        self.wd.getLabelWidget(HOME_NOTE).config(font=('Comic Sans', '9', 'italic'))

        self.wd.addLabelAutoEntry(SEARCH, ['the', 'tue'], row=3, column=2)
        self.wd.addButton(VIEW_PROFILE, self.view_profile, row=3, column=3)

        self.wd.addLabel(dummy, row=4, column=2)
        self.wd.removeLabel(dummy)
        self.wd.addLabel(dummy, row=5, column=2)
        self.wd.removeLabel(dummy)

        self.wd.stopLabelFrame()
        self.wd.setLabelFrameWidth(HOME, 900)

        self.wd.startLabelFrame(FRIENDS, row=1, column=0, rowspan=3, colspan=1, sticky='news')
        self.wd.startScrollPane(FRIENDS, sticky='w')

        self.wd.stopScrollPane()
        self.wd.setScrollPaneWidth(FRIENDS, 0)
        self.wd.stopLabelFrame()

        self.wd.startTabbedFrame(FEATURES, row=1, column=1, rowspan=3, colspan=2)

        self.wd.startTab(BLOG)
        self.wd.startScrollPane(BLOG, disabled='horizontal')
        self.wd.addTextArea(BLOG_INP)
        self.wd.setTextAreaWidth(BLOG_INP, 55)
        self.wd.addButton(POST, self.post_blog)
        self.wd.setButtonSticky(POST, 'left')
        self.wd.addLabel('Your blogs:')
        self.wd.stopScrollPane()
        self.wd.stopTab()

        self.wd.startTab(PROFILE_VIEWER)
        self.wd.addImage(PROFILE_AVATAR, 'assets/default-avatar.png')
        self.wd.setImageSize(PROFILE_AVATAR, 100, 100)
        self.wd.addMessage(PROFILE_USERNAME, HOME_EMAIL)
        self.wd.setMessageWidth(PROFILE_USERNAME, 450)
        self.wd.addMessage(PROFILE_DOB, 'Jan 01, 1990')
        self.wd.setMessageWidth(PROFILE_DOB, 450)
        self.wd.addButton(PROFILE_ADD_FRIEND, self.add_friend)
        self.wd.addLabel(PROFILE_BLOG)
        self.wd.addMessage(PROFILE_BLOG)
        self.wd.setMessageWidth(PROFILE_BLOG, 500)
        self.wd.stopTab()

        self.wd.stopTabbedFrame()
        self.wd.setTabbedFrameWidth(FEATURES, 500)

        self.wd.startLabelFrame('DummyContainer4', row=2)
        self.wd.stopLabelFrame()
        self.wd.startLabelFrame('DummyContainer5', row=3)
        self.wd.stopLabelFrame()
        self.wd.startLabelFrame('DummyContainer6', row=1, column=2)
        self.wd.stopLabelFrame()
        self.wd.removeLabelFrame('DummyContainer4')
        self.wd.removeLabelFrame('DummyContainer5')
        self.wd.removeLabelFrame('DummyContainer6')

        self.chat_wds = dict()
        self.users = set()
        self.friends = set()
        self.blogs = list()
        self.blogs_ui = list()

    def add_friend_ui(self, friend, avatar):
        friend_avatar = friend + ' - avatar'
        chat = friend + CHAT_SUFFIX
        view_profile = friend + VIEW_PROFILE_SUFFIX

        self.wd.startLabelFrame(friend)
        self.wd.setLabelFramePadding(friend, 5, 5)

        self.wd.addImage(friend_avatar, avatar)
        self.wd.setImageSize(friend_avatar, 50, 50)
        self.wd.shrinkImage(friend_avatar, 2)

        self.wd.addLabel(friend + 'dummy1', ' ', row=0, column=1)
        self.wd.addImageButton(chat, self.chat, 'assets/icon-chat.png', row=0, column=2)
        self.wd.setButtonTooltip(chat, 'Chat')

        self.wd.addLabel(friend + 'dummy2', ' ', row=0, column=3)
        self.wd.addImageButton(view_profile, self.view_profile, 'assets/icon-info.png', row=0, column=4)
        self.wd.setButtonTooltip(view_profile, 'View profile')

        self.wd.stopLabelFrame()

    def receive_init_info(self, users, friends, avatars, profile, latest_blog, blogs):
        print('hhh')
        self.users = set(users)
        self.wd.changeAutoEntry(SEARCH, users)

        self.friends = set(friends)

        self.wd.openScrollPane(FRIENDS)

        for i in range(len(friends)):
            friend = friends[i]
            avatar = avatars[i]

            self.add_friend_ui(friend, avatar)
        
        self.wd.stopScrollPane()  

        self.receive_profile(profile[0], profile[1], profile[2], latest_blog)    
        self.wd.setTabbedFrameSelectedTab(FEATURES, BLOG)

        self.wd.openLabelFrame(HOME)
        self.wd.setImage(AVATAR, profile[2])
        self.wd.stopLabelFrame()   

        self.receive_blogs(blogs)

    def change_avatar(self):
        new_avatar = self.wd.openBox('Select a new avatar', dirName='./', fileTypes=[('images', '*.png'), ('images', '*.jpg'), ('images', '*.gif')])
        
        if new_avatar != '':
            self.wd.setImage(AVATAR, new_avatar)
            self.client.send(make_msg(REQUEST.CHANGE_AVATAR, (self.user, new_avatar)))

    def view_profile(self, caller):
        if caller == VIEW_PROFILE:
            pivot = self.wd.getEntry(SEARCH)
            if pivot == '':
                return
            if pivot not in self.users:
                self.wd.errorBox('Invalid input to get user profile', 'The username/email you has typed in does not exist!\nPlease check your input and try again!')
                return

        elif caller == HOME_EMAIL:
            pivot = self.user

        else:
            pivot = self.strip(caller, VIEW_PROFILE_SUFFIX)

        self.client.send(make_msg(REQUEST.GET_PROFILE, pivot))

    def receive_profile(self, username, dob, avatar, latest_blog):
        self.wd.openTab(FEATURES, PROFILE_VIEWER)

        self.wd.setMessage(PROFILE_USERNAME, username)
        self.wd.setMessage(PROFILE_DOB, dob)
        self.wd.setImage(PROFILE_AVATAR, avatar)

        if username == self.user:
            self.wd.hideButton(PROFILE_ADD_FRIEND)
        else:
            self.wd.showButton(PROFILE_ADD_FRIEND)
            self.wd.enableButton(PROFILE_ADD_FRIEND)
            self.wd.setButton(PROFILE_ADD_FRIEND, 'Add Friend')

            if username in self.friends:
                self.wd.setButton(PROFILE_ADD_FRIEND, 'You are already friend')
                self.wd.disableButton(PROFILE_ADD_FRIEND)

        if latest_blog is None:
            self.wd.hideMessage(PROFILE_BLOG)
            self.wd.setLabel(PROFILE_BLOG, 'No blog available!')
        else:
            time, text = latest_blog
            self.wd.setLabel(PROFILE_BLOG, 'Latest blog:')
            self.wd.showMessage(PROFILE_BLOG)
            self.wd.setMessage(PROFILE_BLOG, '(%s)\n%s' % (time, text))

        self.wd.stopTab()
        self.wd.setTabbedFrameSelectedTab(FEATURES, PROFILE_VIEWER)

    def strip(self, parent, suffix):
        return parent[:-len(suffix)]

    def chat(self, caller):
        sender = self.user
        receiver = self.strip(caller, CHAT_SUFFIX)
        self.client.send(make_msg(REQUEST.GET_CHATS, (sender, receiver)))
        
    def confirm_chat(self, chatter1, chatter2, chats):
        if chatter1 == self.user:
            sender, receiver = chatter1, chatter2
        else:
            sender, receiver = chatter2, chatter1

        uuid = str(uuid4())
        chatwd = sender + ' - ' + receiver + ' - ' + uuid
        chat_area = chatwd + CHAT_SUFFIX
        self.chat_wds[receiver] = (chatwd, chat_area)

        self.wd.startSubWindow(chatwd, 'Chat')
        self.wd.setSize(500, 450)

        chat_title = 'From %s (right, blue)\nTo %s (left, red)' % (sender, receiver)
        chat_title_key = chatwd + chat_title
        self.wd.addMessage(chat_title_key, chat_title)
        self.wd.setMessageWidth(chat_title_key, 450)

        self.wd.startScrollPane(chat_area, disabled='horizontal', sticky='w')
        dummy = chatwd + 'dummy'
        self.wd.addLabel(dummy, '---' * 22)

        for i in range(len(chats)):
            chat, who = chats[i]
            chatid = chatwd + '%d' % i
            self.add_chat_message(chatid, chat, who == sender)            

        self.wd.stopScrollPane()
        self.wd.getScrollPaneWidget(chat_area).canvas.yview_moveto(1.0)

        chat_inp = chatwd + INP_SUFFIX
        self.wd.addEntry(chat_inp)
        self.wd.setEntryDefault(chat_inp, 'Type and press ENTER to chat')
        self.wd.setEntrySticky(chat_inp, 'both')
        self.wd.setEntrySubmitFunction(chat_inp, self.send_chat)

        self.wd.setPadding(0, 0)
        self.wd.stopSubWindow()
        self.wd.showSubWindow(chatwd)

    def add_chat_message(self, chatid, text, right):
        self.wd.addMessage(chatid, text)
        self.wd.setMessageWidth(chatid, 300)
        self.wd.setMessageRelief(chatid, 'raised')
            
        if right:
            self.wd.setMessageSticky(chatid, 'right')
            self.wd.setMessageBg(chatid, 'light sky blue')
        else:
            self.wd.setMessageSticky(chatid, 'left')
            self.wd.setMessageBg(chatid, 'salmon')

    def send_chat(self, caller):
        chatwd = self.strip(caller, INP_SUFFIX)
        self.wd.openSubWindow(chatwd)
        text = self.wd.getEntry(caller)
        self.wd.setEntry(caller, '')
        self.wd.stopSubWindow()
        tmp = caller.split(' - ')
        self.client.send(make_msg(REQUEST.CHAT, (tmp[0], tmp[1], text)))

    def receive_chat(self, sender, receiver, text):
        chatwd, chat_area = self.chat_wds[receiver] if sender == self.user else self.chat_wds[sender]
        self.wd.openSubWindow(chatwd)
        self.wd.openScrollPane(chat_area)
        self.add_chat_message(text + str(uuid4()), text, sender == self.user)
        self.wd.stopScrollPane()
        self.wd.getScrollPaneWidget(chat_area).canvas.yview_moveto(1.0)
        self.wd.stopSubWindow()

    def receive_blogs(self, blogs):
        self.wd.openTab(FEATURES, BLOG)
        self.wd.openScrollPane(BLOG)

        self.blogs = blogs
        self.blogs.reverse()

        for element in self.blogs_ui:
            self.wd.removeMessage(element)
            self.wd.removeButton(element)
            self.wd.removeLabel(element + 'empty')
        self.blogs_ui = []

        for i in range(len(self.blogs)):
            time, text = self.blogs[i]
            blog_key = ('%d' % i) + BLOG
            self.blogs_ui.append(blog_key)
            self.wd.addMessage(blog_key, '(%s)\n%s' % (time, text))
            self.wd.setMessageWidth(blog_key, 500)
            self.wd.setMessageSticky(blog_key, 'both')
            self.wd.setMessageRelief(blog_key, 'raised')
            self.wd.setMessageAlign(blog_key, 'left')
            self.wd.addButton(blog_key, self.share_blog)
            self.wd.setButton(blog_key, 'Share')
            self.wd.setButtonSticky(blog_key, 'left')
            self.wd.addEmptyLabel(blog_key + 'empty')

        self.wd.stopScrollPane()
        self.wd.stopTab()

    def post_blog(self):
        self.wd.openTab(FEATURES, BLOG)
        self.wd.openScrollPane(BLOG)
        text = self.wd.getTextArea(BLOG_INP)
        self.wd.clearTextArea(BLOG_INP)
        self.wd.stopScrollPane()
        self.wd.stopTab()

        if text != '':
            time = str(datetime.now()) + ' - ' + self.user
            self.client.send(make_msg(REQUEST.POST_BLOG, (self.user, time, text)))

    def share_blog(self, caller):
        blog_index = int(self.strip(caller, BLOG))
        time, text = self.blogs[blog_index]
        self.client.send(make_msg(REQUEST.SHARE_BLOG, (self.user, time, text)))

    def add_friend(self):
        self.wd.openTab(FEATURES, PROFILE_VIEWER)
        pivot = self.wd.getMessage(PROFILE_USERNAME)
        self.wd.stopTab()

        self.client.send(make_msg(REQUEST.ADD_FRIEND, (self.user, pivot)))

    def ask_confirm_friend(self, data):
        reply = self.wd.questionBox('Friend request from %s' % data[0], 'Do you want to be friend with %s?' % data[0])
        self.client.send(make_msg(REQUEST.CONFIRM_FRIEND, (data[0], data[1], reply)))

    def receive_friend_request_reply(self, origin, friend, reply, avatar):
        if reply:
            if friend != self.user:
                self.wd.infoBox('Friend request accepted from %s' % friend, 'You and %s are now friends!' % friend)
                self.wd.openScrollPane(FRIENDS)
                self.add_friend_ui(friend, avatar)
                self.wd.stopScrollPane()
            else:
                self.wd.openScrollPane(FRIENDS)
                self.add_friend_ui(origin, avatar)
                self.wd.stopScrollPane()

        else:
            if friend != self.user:
                self.wd.errorBox('Friend request rejected from %s' % friend, '%s does not want to be friend with you!' % friend)

    def open(self):
        if self.client is not None:
            self.client.send(make_msg(REQUEST.GET_INIT_INFO, self.user))
        self.wd.go()

    def close(self):
        self.wd.stop()