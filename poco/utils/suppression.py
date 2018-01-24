# coding=utf-8
__author__ = 'lxn3032'


import warnings
from functools import wraps


def deprecated(message):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            warnings.warn("Deprecation Warning: " + message)
            return func(*args, **kwargs)
        return wrapped
    return wrapper
