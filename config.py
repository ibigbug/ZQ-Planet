#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import scoped_session, sessionmaker
from models import * # import for bind
import memcache

db = scoped_session(sessionmaker(bind=engine))

mem_config = {
    "HOST" : "127.0.0.1:11211",
    "DEBUG" : True
}
cache = memcache.Client([mem_config["HOST"]],debug=mem_config["DEBUG"])
