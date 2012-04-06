#!/usr/bin/env python

from tornado.web import RequestHandler
from tornado.options import options
from models.mixin import UserMixin
from lib.filters import xmldatetime
from lib.utils import DictedObj

import datetime

class BaseHandler(RequestHandler, UserMixin):
    def prepare(self):
        self._prepare_context()
        self._prepare_filters()

    def finish(self, chunk=None):
        super(BaseHandler, self).finish(chunk)
        if self.get_status() == 500:
            try:
                self.db.commit()
            except:
                self.db.rollback()
            finally:
                self.db.commit()

    @property
    def db(self):
        return self.application.db

    @property
    def cache(self):
        return self.application.cache

    def render_string(self, template_name, **kwargs):
        kwargs.update(self._filters)
        assert "context" not in kwargs, "context is a reserved keyword."
        kwargs["context"] = self._context
        return super(BaseHandler, self).render_string(template_name, **kwargs)

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

    def _prepare_context(self):
        self._context = DictedObj()
        self._context.now = datetime.datetime.utcnow()
        self._context.sitename = options.sitename
        self._context.siteurl = options.siteurl
        self._context.debug = options.debug

    def _prepare_filters(self):
        self._filters = DictedObj()
        self._filters.xmldatetime = xmldatetime
