# coding=utf-8
from __future__ import unicode_literals

import numbers

from poco.sdk.interfaces.hierarchy import HierarchyInterface
from poco.sdk.interfaces.input import InputInterface
from poco.sdk.interfaces.screen import ScreenInterface
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
    def getAttr(self, nodes, name):
        return self.attributor.getAttr(nodes, name)

    @transform_node_has_been_removed_exception
    def setAttr(self, nodes, name, value):
        return self.attributor.setAttr(nodes, name, value)

    def select(self, query, multiple=False):
        return self.selector.select(query, multiple)

    def dump(self):
        return self.dumper.dumpHierarchy()


class AndroidScreen(ScreenInterface):
    def __init__(self, remote):
        super(AndroidScreen, self).__init__()
        self.remote = remote

    def getScreen(self, width=720):
        # snapshot接口暂时还补统一
        if not isinstance(width, numbers.Number):
            raise TypeError('width should be numbers/')

        return self.remote.getScreen(int(width))

    def getPortSize(self):
        return self.remote.getPortSize()


class AndroidInput(InputInterface):
    def __init__(self, remote):
        super(AndroidInput, self).__init__()
        self.remote = remote

    def click(self, x, y):
        self.remote.click(float(x), float(y))

    def swipe(self, x1, y1, x2, y2, duration=2.0):
        self.remote.swipe(float(x1), float(y1), float(x2), float(y2), float(duration))

    def longClick(self, x, y, duration=3.0):
        self.remote.longClick(float(x), float(y), float(duration))
