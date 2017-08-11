# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:34:46

from poco.interfaces.hierarchy import HierarchyInterface
from poco.vendor.hrpc.utils import transform_node_has_been_removed_exception


class RemotePocoHierarchy(HierarchyInterface):
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
