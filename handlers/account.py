#!/usr/bin/env python

from tornado.options import options
from lib.handler import BaseHandler
from models.mixin import UserMixin
from config import db


class LoginHandler(BaseHandler, UserMixin):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        raw = self.get_argument("password")
        user = self.get_user_by_name(username)
        if not user.token:
            user.token = user.password.split('$')[0]
            self.db.add(user)
            self.db.commit()
        auth = self.check_password(username, raw)
        if auth:
            self.set_secure_cookie("user","%s$%s" % (user.id,user.token))
            return self.redirect("/feed/add")
        return self.render("login.html")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        return self.redirect("/")



handlers = [
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
]
