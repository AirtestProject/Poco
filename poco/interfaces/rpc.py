# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:25:58


__all__ = ['RpcInterface', 'RpcRemoteException', 'RpcTimeoutException']


def required(func):
    return func


class RpcInterface(object):
    """Base Rpc Client"""
    def __init__(self):
        super(RpcInterface, self).__init__()

    # node/hierarchy interface
    @required
    def getattr(self, nodes, name):
        """get node attribute"""
        raise NotImplementedError

    @required
    def setattr(self, nodes, name, val):
        """set node attribute"""
        raise NotImplementedError

    @required
    def select(self, query, multiple=False):
        """select nodes by query"""
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError

    def evaluate(self, obj_proxy):
        """
        临时接口，排除bug后移除
        返回对象本身即可

        :param obj_proxy: 
        :return: 
        """
        return obj_proxy

    # input interface
    def click(self, x, y):
        raise NotImplementedError

    def long_click(self, x, y, duration):
        raise NotImplementedError

    def swipe(self, x1, y1, x2, y2, duration):
        raise NotImplementedError

    def get_input_panel_size(self):
        return self.get_screen_size()

    # screen interface
    @required
    def get_screen_size(self):
        raise NotImplementedError

    def get_screen(self):
        raise NotImplementedError


class RpcRemoteException(Exception):
    pass


class RpcTimeoutException(Exception):
    pass
