#!/usr/bin/env python

import functools
import logging
from tornado.options import options

class login_required(object):
    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(handler,*args,**kwargs):
            if not handler.current_user:
                return handler.redirect(options.login_url)
            else:
                return method(handler,*args,**kwargs)
        return wrapper


class cache(object):
    def __init__(self, prefix, time=0):
        self.prefix = prefix
        self.time = time

    def __call__(self, method):
        @functools.wraps(method)
        def wrapper(handler, *args, **kwargs):
            if not handler.cache:
                return method(*args,**kwargs)

            if args:
                key = self.prefix + ':' + '-'.join(str(a) for a in args)
            else:
                key = self.prefix
            if kwargs:
                for k,v in kwargs.iteritems():
                    key += '%s#%s' % (k,v)
            value = handler.cache.get(key)
            if value is None:
                value = method(handler,*args,**kwargs)
                try:
                    handler.cache.set(key,value,self.time)
                except:
                    logging.warn('cache error at: %s' % key)
                    pass
            return value
        return wrapper
