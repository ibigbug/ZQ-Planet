#!/usr/bin/env python

from tornado.options import options
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from config import db

class User(db.Model):
    username = Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)
    token = Column(String(32), nullable=True)


    def __repr__(self):
        return "<User ('%s')>" % (self.username)


class Feed(db.Model):
    feed_name = Column(String(100), nullable=False)
    feed_url = Column(String(100), nullable=False)

    def __repr__(self):
        return "<Feed ('%s')>" % (self.feed_name)


class Entry(db.Model):
    entry_title = Column(String(100), nullable=False)
    entry_link = Column(String(300), nullable=False)
    entry_content = Column(Text, nullable=False)
    entry_author = Column(String(100), nullable=False)
    entry_pubdate = Column(String(100),nullable=True)
    entry_parrent = Column(Integer(11),nullable=False)

    def __repr__(self):
        return "<Entry ('%s')>" % (self.entry_title)
