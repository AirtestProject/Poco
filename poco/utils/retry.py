# coding=utf-8
__author__ = 'lxn3032'

import time
import functools


def retries_when(exctypes, count=3, delay=0.0):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            ex = None
            for i in range(count):
                try:
                    return func(*args, **kwargs)
                except exctypes as e:
                    ex = e
                    time.sleep(delay)
            if ex:
                raise ex
        return wrapped
    return wrapper
