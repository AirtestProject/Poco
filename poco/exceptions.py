# coding=utf-8
from __future__ import unicode_literals

import six


__author__ = 'lxn3032'


class PocoException(Exception):

    def __str__(self):
        if six.PY2:
            if isinstance(self.message, unicode):
                return self.message.encode("utf-8")
            else:
                return self.message
        else:
            if isinstance(self.message, bytes):
                return self.message.decode('utf-8')
            else:
                return self.message

    __repr__ = __str__


class InvalidOperationException(PocoException):
    """
    操作无效
    通常超出屏幕之外的点击或者滑动会判定为操作无效
    """

    pass


class PocoTargetTimeout(PocoException):
    def __init__(self, action, poco_obj_proxy):
        super(PocoTargetTimeout, self).__init__()
        self.message = 'Timeout when waiting for {} of "{}"'.format(action, poco_obj_proxy)


class PocoNoSuchNodeException(PocoException):
    def __init__(self, objproxy):
        super(PocoNoSuchNodeException, self).__init__()
        self.message = 'Cannot find any visible node by query {}'.format(objproxy)


class PocoTargetRemovedException(PocoException):
    def __init__(self, action, objproxy):
        super(PocoTargetRemovedException, self).__init__()
        self.message = 'Remote ui object "{}" has been removed from hierarchy during {}.'.format(objproxy, action)
