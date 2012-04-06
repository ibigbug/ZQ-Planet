#!/usr/bin/env python

from handlers import account
from handlers import dashboard
from handlers import admin

handlers = []
handlers.extend(account.handlers)
handlers.extend(dashboard.handlers)
handlers.extend(admin.handlers)

ui_modules = {}
