#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import options

from lib.database import SQLAlchemy
import memcache

db = SQLAlchemy(options.database, pool_recycle=3600, echo=options.debug)
cache = memcache.Client(options.memcache.split(),debug=options.debug)
