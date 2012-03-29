#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import create_all, User
from models.mixin import UserMixin
from config import db

if __name__ == "__main__":
    create_all()
    c = raw_input("Create Super User?(y/n)")
    if c == "n":
        import sys
        sys.exit(1)
    username = raw_input("username:")
    import getpass
    raw = getpass.getpass("password:")
    UserMixin.create_user(username,raw)
    print "Finished!!!"
