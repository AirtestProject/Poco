# coding=utf-8
from __future__ import unicode_literals
__author__ = 'lxn3032'


class PocoException(Exception):

    def __str__(self):
        return self.msg.encode("utf-8")


class InvalidOperationException(PocoException):
    """
    操作无效
    通常超出屏幕之外的点击或者滑动会判定为操作无效
    """
    pass


class PocoTargetTimeout(PocoException):
    def __init__(self, action, poco_obj_proxy):
        self.msg = 'Timeout when waiting for {} of "{}"'.format(action, poco_obj_proxy)


class PocoNoSuchNodeException(PocoException):
    def __init__(self, objproxy):
        self.msg = 'Cannot find any visible node by query {}'.format(objproxy)


class PocoTargetRemovedException(PocoException):
    def __init__(self, action, objproxy):
        self.msg = 'Remote ui object "{}" has been removed from hierarchy during {}.'.format(objproxy, action)
