#!/usr/bin/env python

from tornado.options import options
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, Text
engine = create_engine(options.database, echo=options.debug)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    password = Column(String(100), nullable=False)
    token = Column(String(32), nullable=False)


    def __repr__(self):
        return "<User ('%s')>" % (self.username)


class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True)
    feed_name = Column(String(100), nullable=False)
    feed_url = Column(String(100), nullable=False)

    def __repr__(self):
        return "<Feed ('%s')>" % (self.feed_name)


class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    entry_title = Column(String(100), nullable=False)
    entry_link = Column(String(300), nullable=False)
    entry_content = Column(Text, nullable=False)
    entry_author = Column(String(100), nullable=False)
    entry_pubdate = Column(String(100),nullable=True)
    entry_parrent = Column(Integer(11),nullable=False)

    def __repr__(self):
        return "<Entry ('%s')>" % (self.entry_title)


users_table = User.__tablename__
feeds_table = Feed.__tablename__
entry_table = Entry.__tablename__

metadata = Base.metadata

def create_all():
    metadata.create_all(engine)
