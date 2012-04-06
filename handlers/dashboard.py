#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado.escape import *
from models.mixin import *
from models import Entry
from lib.handler import BaseHandler
from lib.decorators import cache

import datetime


class MainHandler(BaseHandler, FeedMixin, EntryMixin):
    @cache('initfeed')
    def get(self):
        feeds = self.feed_list
        return self.render("index.html",feeds=feeds)

    @cache('fetchfeed')
    def post(self):
        id = self.get_argument("id")
        entrys = recursive_unicode(self.json_format(id=id))
        self.write(entrys)
        self.finish()


class ViewHandler(BaseHandler, FeedMixin, EntryMixin):
    def get(self, id):
        id = int(id) 
        entry = Entry.query.filter_by(id=id).first()
        if not entry:
            return self.send_error(404)
        previous = entry.entry_parrent 
        return self.render("view.html",entry=entry,previous=previous)


class FeedHandler(BaseHandler):
    @cache('feed',1800)
    def get(self):
        self.set_header('Content-Type', 'text/xml; charset=utf-8')
        entrys = Entry.query.order_by('-id')[:20]
        now = datetime.datetime.utcnow()
        html =  self.render_string('feed.xml',now=now,entrys=entrys)
        self.finish(html)


handlers = [
    (r"/",MainHandler),
    (r"/view/(\d+)",ViewHandler),
    (r"/feed",FeedHandler),
]
