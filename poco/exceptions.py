# coding=utf-8
__author__ = 'lxn3032'


class InvalidOperationException(Exception):
    """
    操作无效
    通常超出屏幕之外的点击或者滑动会判定为操作无效
    """
    pass
