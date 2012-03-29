#!/usr/bin/env python

from handlers import account
from handlers import dashboard
from handlers import feed

handlers = []
handlers.extend(account.handlers)
handlers.extend(dashboard.handlers)
handlers.extend(feed.handlers)

ui_modules = {}
