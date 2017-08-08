# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:25:58

import types

from poco.sdk.Attributor import Attributor
from poco.sdk.Selector import Selector


__all__ = ['RpcInterface', 'RpcRemoteException', 'RpcTimeoutException']


class RpcInterface(object):
    """Base Rpc Client"""
    def __init__(self, dumper=None, selector=None, attributor=None, inputer=None, screen=None):
        super(RpcInterface, self).__init__()
        self.dumper = dumper
        if not isinstance(dumper, types.NoneType) and isinstance(selector, types.NoneType):
            self.selector = Selector(self.dumper)
        else:
            self.selector = selector
        if isinstance(attributor, types.NoneType):
            self.attributor = Attributor()
        else:
            self.attributor = attributor
        self.inputer = inputer
        self.screen = screen

    # node/hierarchy interface
    def getattr(self, nodes, name):
        """get node attribute"""
        return self.attributor.getAttr(nodes, name)

    def setattr(self, nodes, name, value):
        """set node attribute"""
        return self.attributor.setAttr(nodes, name, value)

    def select(self, query, multiple=False):
        """select nodes by query"""
        if isinstance(self.selector, types.NoneType):
            raise NotImplementedError
        return self.selector.select(query, multiple)

    def dump(self):
        if isinstance(self.dumper, types.NoneType):
            raise NotImplementedError
        raise self.dumper.dumpHierarchy()

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
        if isinstance(self.inputer, types.NoneType):
            raise NotImplementedError
        self.inputer.click(x, y)

    def long_click(self, x, y, duration):
        if isinstance(self.inputer, types.NoneType):
            raise NotImplementedError
        self.inputer.longClick(x, y, duration)

    def swipe(self, x1, y1, x2, y2, duration):
        if isinstance(self.inputer, types.NoneType):
            raise NotImplementedError
        self.inputer.swipe(x1, y1, x2, y2, duration)

    # screen interface
    def get_screen_size(self):
        """
        获取渲染屏幕的尺寸，type float
        :return: [width, height] as floats 
        """

        if isinstance(self.screen, types.NoneType):
            raise NotImplementedError
        return self.screen.getPortSize()

    def get_screen(self, width):
        if isinstance(self.screen, types.NoneType):
            raise NotImplementedError
        return self.screen.getScreen(width)


class RpcRemoteException(Exception):
    pass


class RpcTimeoutException(Exception):
    pass
