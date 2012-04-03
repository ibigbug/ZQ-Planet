#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tornado.escape import *
from models.mixin import *
from models import Entry
from lib.handler import BaseHandler
from lib.decorators import cache

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


handlers = [
    (r"/",MainHandler),
    (r"/view/(\d+)",ViewHandler),
]
