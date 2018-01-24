# coding=utf-8
from functools import wraps


class RemoteError(Exception):
    pass


def sync_wrapper(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        cb = func(*args, **kwargs)
        ret, err = cb.wait(timeout=30)
        if err:
            raise RemoteError(err['message'])
        return ret
    return new_func
