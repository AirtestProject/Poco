# coding=utf-8
from functools import wraps


def sync_wrapper(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        cb = func(*args, **kwargs)
        ret, err = cb.wait(timeout=5)
        if err:
            # FIXME: 远端报错时，err为dict，此处无法抛出
            # cb.wait里要处理这个err
            print err['message']
            raise err
        return ret
    return new_func
