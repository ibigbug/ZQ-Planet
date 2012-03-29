#!/usr/bin/env python

from tornado.web import RequestHandler
from models.mixin import UserMixin

class BaseHandler(RequestHandler, UserMixin):
    @property
    def db(self):
        return self.application.db

    @property
    def cache(self):
        return self.application.cache

    def get_current_user(self):
        cookie = self.get_secure_cookie("user")
        if not cookie:
            return None
        try:
            uid, token = cookie.split("$")
            uid = int(uid)
        except:
            self.clear_cookie("user")
            return None
        user = self.get_user_by_uid(uid)
        if not user:
            return None
        if user.token == token:
            return user
        self.clear_cookie("user")
        return None
