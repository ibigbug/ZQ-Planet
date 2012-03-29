from random import choice
import hashlib

from models import User, Feed, Entry
from config import db


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
        return db.query(User).filter_by(id=uid).all()[0]
    
    def get_user_by_name(self, username):
        user = db.query(User).filter_by(username=username).all()[0]
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
        user = User(username=username,password=password,token=token)
        db.add(user)
        db.commit()


class FeedMixin(object):
    @staticmethod
    def save_feed(feed_name,feed_url,feed_author=None):
        feed =Feed(feed_name=feed_name,feed_url=feed_url)
        if feed_author:
            feed.feed_author=feed_author
        db.add(feed)
        db.commit()


    @staticmethod
    def delete_feed(id):
        feed = db.query(Feed).filter_by(id=id).one()
        db.delete(feed)
        db.commit()

    @property
    def feed_list(self):
        return db.query(Feed).all()

    
class EntryMixin(object):
    @staticmethod
    def save_entry(entry_title,entry_link,entry_author,entry_pubdate,
                   entry_parent_id):
        entry =\
        Entry(entry_title,entry_content,entry_author,entry_pubdate,entry_parent)
        db.add(entry)
        db.commit()


    @property
    def entrys(self):
        return db.query(Entry).all()

    def get_entry_by_id(self, id):
        entry = db.query(Entry).filter_by(entry_parrent=id).all()
        return entry

    def json_format(self,id):
        entrys = db.query(Entry).filter_by(entry_parrent=id).all()
        count = db.query(Entry).filter_by(entry_parrent=id).count()
        json = {'status':'OK','count':count,'data':[]}
        for e in entrys:
            _json = [{
                'title': e.entry_title,
                'link': e.entry_link,
                'content': e.entry_content,
                'author': e.entry_author,
                'time': e.entry_pubdate
            }]
            json['data'].extend(_json)
        return json
