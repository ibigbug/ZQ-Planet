#!/usr/bin/env python
# -*- coding: utf-8 -*-

import app
from models import User
from models.mixin import UserMixin
from config import db
from argparse import ArgumentParser

def syncdb():
    db.create_db()

def create_super_user():
    c = raw_input("Create Super User?(y/n)")
    if c == "n":
        import sys
        sys.exit(1)
    username = raw_input("username:")
    import getpass
    raw = getpass.getpass("password:")
    user = User()
    user.username = username
    user.password = UserMixin.create_password(raw)
    db.session.add(user)
    db.session.commit()
    print "Finished!!!"

def init():
    syncdb()
    create_super_user()

def main():
    p = ArgumentParser(usage='-syncdb || -createuser', 
                       description='For syncdb and create super user')
    p.add_argument(dest='cmd',nargs='*')
    args = p.parse_args()

    if not args.cmd:
        return init()
    def run_command(cmd):
        if cmd == 'syncdb':
            return syncdb()
        if cmd == 'createuser':
            return create_super_user()
    if isinstance(args.cmd, basestring):
        return run_command(args.cmd)
    if isinstance(args.cmd, (list, tuple)):
        for cmd in args.cmd:
            run_command(cmd)


if __name__ == "__main__":
    main()
