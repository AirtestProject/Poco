# coding=utf-8

from functools import wraps

from airtest.core.main import touch, swipe, snapshot


def airtestlog(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        snapshot(msg=unicode(self._last_proxy))
        return func(self, *args, **kwargs)
    return wrapper
