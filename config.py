#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import options
from models import * # import for bind
import memcache

db = scoped_session(sessionmaker(bind=engine))

cache = memcache.Client(options.memcache.split(),debug=options.debug)
