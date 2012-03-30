#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from tornado.options import options
from tornado.escape import *
from models.mixin import FeedMixin, EntryMixin
from models import Entry
from lib.handler import BaseHandler
from lib.decorators import login_required
from time import mktime
from datetime import datetime
import feedparser

class AddHandler(BaseHandler,FeedMixin):
    @login_required()
    def get(self):
        return self.render("feed_add.html")

    @login_required()
    def post(self):
        feed_name = self.get_argument("feed_name")
        feed_url = self.get_argument("feed_url")
        self.save_feed(feed_name,feed_url)
        return self.redirect("/feed/view")


class ViewHandler(BaseHandler,FeedMixin):
    @login_required()
    def get(self):
        entry = self.feed_list
        return self.render("feed_view.html",entry=entry)

    @login_required()
    def post(self):
        feeds = self.get_arguments("id")
        for f in feeds:
            self.delete_feed(f)
        entry = self.feed_list
        return self.render("feed_view.html",entry=entry)


class FetchHandler(BaseHandler,FeedMixin,EntryMixin):
    @login_required()
    def get(self):
        self.write(u"抓取中")
        self.finish()
        feeds = self.feed_list
        for f in feeds:
            d  = feedparser.parse(f.feed_url)
            for e in d.entries:
                exist =\
                self.db.query(Entry).filter_by(entry_title=to_unicode(e.title)).first()
                if exist:
                    continue
                entry = Entry(entry_title=to_unicode(e.title))
                entry.entry_author = to_unicode(e.author)
                entry.entry_link = to_unicode(e.link)
                entry.entry_content = to_unicode(e.description)
                entry.entry_parrent = f.id
                entry.entry_pubdate =\
                datetime.fromtimestamp(mktime(e.updated_parsed))
                self.db.add(entry)
                self.db.commit()
    
handlers = [
    (r"/feed/add",AddHandler),
    (r"/feed/view",ViewHandler),
    (r"/feed/fetch",FetchHandler),
]
