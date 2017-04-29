# coding=utf-8
__author__ = 'lxn3032'


import functools


def retries_when(exctypes, count=3):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            ex = None
            for i in range(count):
                try:
                    return func(*args, **kwargs)
                except exctypes as e:
                    ex = e
            raise ex
        return wrapped
    return wrapper
