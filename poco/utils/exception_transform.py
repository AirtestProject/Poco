# coding=utf-8
from __future__ import unicode_literals

import types
from functools import wraps

__author__ = 'lxn3032'


def member_func_exception_transform(Origin, Target):
    def wrapper(Cls):
        class WrapperCls(Cls):
            def __getattribute__(self, item):
                func = super(WrapperCls, self).__getattribute__(item)
                if isinstance(func, types.FunctionType) and not item.startswith('_'):
                    @wraps(func)
                    def wrapped(*args, **kwargs):
                        try:
                            return func(*args, **kwargs)
                        except Origin as e:
                            raise Target(e)
                    return wrapped
                else:

                    return func

        WrapperCls.__name__ = Cls.__name__
        return WrapperCls
    return wrapper


def exception_transform(Origin, Target):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Origin as e:
                raise Target(e)
        return wrapped
    return wrapper
