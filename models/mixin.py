from random import choice
import hashlib

from models import User, Feed, Entry


class UserMixin(object):
    @staticmethod
    def make_salt(lenght=16):
        number = "1234567890"
        l_case = "abcdefghijklmnopqrstuvwxyz"
        u_case = l_case.upper()
        base = number + l_case + u_case
        salt = "".join([choice(base) for i in range(lenght)])
        return salt

    def get_user_by_uid(self, uid):
        return User.query.filter_by(id=uid).first()
    
    def get_user_by_name(self, username):
        user = User.query.filter_by(username=username).first()
        return user

    @classmethod
    def create_password(self, raw):
        salt = self.make_salt(8)
        hsh = hashlib.sha1(salt + raw).hexdigest()
        return "%s$%s" % (salt, hsh)
    
    def check_password(self, username, raw):
        user = self.get_user_by_name(username)
        salt, hsh = user.password.split("$")
        verify = hashlib.sha1(salt + raw).hexdigest()
        return verify == hsh

    @classmethod
    def create_user(self, username, raw):
        password = self.create_password(raw)
        token = password.split("$")[0]
        user = User()
        user.username = username
        user.password = password
        user.token = token
        self.db.add(user)
        self.db.commit()


class FeedMixin(object):
    def save_feed(self,feed_name,feed_url,feed_author=None):
        feed =Feed(feed_name=feed_name,feed_url=feed_url)
        if feed_author:
            feed.feed_author=feed_author
        self.db.add(feed)
        self.db.commit()


    @staticmethod
    def delete_feed(id):
        feed = db.query(Feed).filter_by(id=id).one()
        self.db.delete(feed)
        self.db.commit()

    @property
    def feed_list(self):
        return self.db.query(Feed).all()

    
class EntryMixin(object):
    @staticmethod
    def save_entry(entry_title,entry_link,entry_author,entry_pubdate,
                   entry_parent_id):
        entry =\
        Entry(entry_title,entry_content,entry_author,entry_pubdate,entry_parent)
        self.db.add(entry)
        self.db.commit()


    @property
    def entrys(self):
        return self.db.query(Entry).all()

    def get_entry_by_id(self, id):
        entry = self.db.query(Entry).filter_by(entry_parrent=id).all()
        return entry

    def json_format(self,id):
        entrys =\
        self.db.query(Entry).filter_by(entry_parrent=id).order_by('-entry_pubdate')
        count = self.db.query(Entry).filter_by(entry_parrent=id).count()
        json = {'status':'OK','count':count,'data':[]}
        for e in entrys:
            _json = [{
                'id' : e.id,
                'title': e.entry_title,
                'link': e.entry_link,
                'content': e.entry_content,
                'author': e.entry_author,
                'time': e.entry_pubdate
            }]
            json['data'].extend(_json)
        return json
