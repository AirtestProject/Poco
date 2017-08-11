# coding=utf-8
from __future__ import unicode_literals

import numbers

from poco.interfaces.hierarchy import HierarchyInterface
from poco.interfaces.screen import ScreenInterface
from poco.interfaces.input import InputInterface
from poco.vendor.hrpc.utils import transform_node_has_been_removed_exception


__author__ = 'lxn3032'


class AndroidHierarchy(HierarchyInterface):
    def __init__(self, dumper, selector, attributor):
        HierarchyInterface.__init__(self)
        self.dumper = dumper
        self.selector = selector
        self.attributor = attributor

    # node/hierarchy interface
    @transform_node_has_been_removed_exception
    def getattr(self, nodes, name):
        return self.attributor.getAttr(nodes, name)

    @transform_node_has_been_removed_exception
    def setattr(self, nodes, name, value):
        return self.attributor.setAttr(nodes, name, value)

    def select(self, query, multiple=False):
        return self.selector.select(query, multiple)

    def dump(self):
        return self.dumper.dumpHierarchy()


class AndroidScreen(ScreenInterface):
    def __init__(self, screen):
        super(AndroidScreen, self).__init__()
        self.screen = screen

    def snapshot(self, width=720):
        # snapshot接口暂时还补统一
        if not isinstance(width, numbers.Number):
            raise TypeError('width should be numbers/')

        return self.screen.getScreen(int(width))

    def get_screen_size(self):
        return self.screen.getPortSize()


class AndroidInput(InputInterface):
    def __init__(self, inputer):
        super(AndroidInput, self).__init__()
        self.inputer = inputer

    def click(self, pos):
        self.inputer.click(*pos)

    def swipe(self, p1, direction, duration=2.0):
        p2 = [p1[0] + direction[0], p1[1] + direction[1]]
        self.inputer.swipe(p1[0], p1[1], p2[0], p2[1], duration)

    def long_click(self, pos, duration=3.0):
        self.inputer.longClick(pos[0], pos[1], duration)
