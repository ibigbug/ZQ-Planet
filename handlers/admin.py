#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.escape import to_unicode
from models.mixin import FeedMixin, EntryMixin
from models import Entry
from lib.handler import BaseHandler
from lib.decorators import login_required
from time import mktime
from datetime import datetime
import feedparser
#import pprint


class AddHandler(BaseHandler, FeedMixin):
    @login_required()
    def get(self):
        return self.render("feed_add.html")

    @login_required()
    def post(self):
        feed_name = self.get_argument("feed_name")
        feed_url = self.get_argument("feed_url")
        self.save_feed(feed_name, feed_url)
        return self.redirect("/admin/view")


class ViewHandler(BaseHandler, FeedMixin):
    @login_required()
    def get(self):
        entry = self.feed_list
        return self.render("feed_view.html", entry=entry)

    @login_required()
    def post(self):
        feeds = self.get_arguments("id")
        for f in feeds:
            self.delete_feed(f)
        entry = self.feed_list
        return self.render("feed_view.html", entry=entry)


class FetchHandler(BaseHandler, FeedMixin, EntryMixin):
    def get(self):
        self.write(u"抓取中<a href='/'>回首页</a>")
        self.finish()
        feeds = self.feed_list
        #pp = pprint.PrettyPrinter(indent=4)
        for f in feeds:
            d = feedparser.parse(f.feed_url)
            for e in d.entries:
                #pp.pprint(e.content[0].value)
                exist =\
                self.db.query(Entry).filter_by(entry_title=\
                to_unicode(e.title)).first()
                if exist:
                    continue
                entry = Entry(entry_title=to_unicode(e.title))
                try:
                    entry.entry_author = to_unicode(e.author)
                except:
                    entry.entry_author = 'admin'
                entry.entry_link = to_unicode(e.link)
                entry_content = to_unicode(e.content[0].value)
                entry.entry_content = entry_content
                entry.entry_parrent = f.id
                entry.entry_pubdate =\
                datetime.fromtimestamp(mktime(e.updated_parsed))
                self.db.add(entry)
                self.db.commit()

handlers = [
    (r"/admin/add", AddHandler),
    (r"/admin/view", ViewHandler),
    (r"/admin/fetch", FetchHandler),
]
