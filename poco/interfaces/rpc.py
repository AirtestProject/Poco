# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:25:58


# deprecated


class RpcInterface(object):
    """Base Rpc Client"""
    def __init__(self, uihierarchy=None, inputer=None, screen=None):
        super(RpcInterface, self).__init__()
        self.ui = uihierarchy
        self.inputer = inputer
        self.screen = screen

    # node/hierarchy interface
    def getattr(self, nodes, name):
        """get node attribute"""
        return self.ui.getattr(nodes, name)

    def setattr(self, nodes, name, value):
        """set node attribute"""
        return self.ui.setattr(nodes, name, value)

    def select(self, query, multiple=False):
        """select nodes by query"""
        return self.ui.select(query, multiple)

    def dump(self):
        return self.ui.dump()

    # input interface
    def click(self, pos):
        self.inputer.click(pos)

    def long_click(self, pos, duration=2):
        self.inputer.longClick(pos, duration)

    def swipe(self, p1, p2=None, direction=None, duration=1):
        self.inputer.swipe(p1, p2, direction, duration)

    # screen interface
    def get_screen_size(self):
        """
        获取渲染屏幕的尺寸，type float
        :return: [width, height] as floats
        """
        return self.screen.getPortSize()

    def get_screen(self, width):
        return self.screen.getScreen(width)
