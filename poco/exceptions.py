# coding=utf-8
__author__ = 'lxn3032'


class InvalidOperationException(Exception):
    """
    操作无效
    通常超出屏幕之外的点击或者滑动会判定为操作无效
    """
    pass


class PocoTargetTimeout(Exception):
    def __init__(self, action, poco_obj_proxy):
        msg = 'Timeout when waiting for {} of "{}"'.format(action, poco_obj_proxy)
        super(PocoTargetTimeout, self).__init__(msg)


class PocoNoSuchNodeException(Exception):
    def __init__(self, query):
        msg = 'Cannot find any visible node by query {}'.format(repr(query))
        super(PocoNoSuchNodeException, self).__init__(msg)
