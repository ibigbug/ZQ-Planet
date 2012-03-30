#!/usr/bin/env python

import os
PROJDIR = os.path.abspath(os.path.dirname(__file__))
ROOTDIR = os.path.split(PROJDIR)[0]

import site
site.addsitedir(ROOTDIR)

import tornado.options
import tornado.locale
from tornado.options import define, options
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado import web

define("port", 8000)
define("debug", True)
define('database', 'mysql://root:123@localhost/feedburner?charset=utf8')
define('memcache', '127.0.0.1:11211')

define("static_path", os.path.join(PROJDIR, "static"))
define("template_path", os.path.join(PROJDIR, "templates"))
define("xsrf_cookies", True)
define("login_url", "/login")
define("cookie_secret", "cookie_secret") 




class Application(web.Application):
    def __init__(self):
        from config import db, cache
        from urls import handlers, ui_modules
        settings = dict(
            debug=options.debug,
            autoescape=None,
            cookie_secret=options.cookie_secret,
            xsrf_cookies=options.xsrf_cookies,
            login_url=options.login_url,

            template_path=options.template_path,
            static_path=options.static_path,

            ui_modules = ui_modules,
        )
        super(Application, self).__init__(handlers, **settings)
        Application.db = db
        Application.cache = cache


def run_server():
    server = HTTPServer(Application(), xheaders=True)
    server.listen(int(options.port))
    IOLoop.instance().start()


if __name__ == "__main__":
    run_server()
