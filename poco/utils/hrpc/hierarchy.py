# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-11 14:34:46

from hrpc.exceptions import TransportDisconnected

from poco.sdk.interfaces.hierarchy import HierarchyInterface
from poco.utils.hrpc.utils import transform_node_has_been_removed_exception
from poco.utils.retry import retries_when


class RemotePocoHierarchy(HierarchyInterface):
    def __init__(self, dumper, selector, attributor):
        super(RemotePocoHierarchy, self).__init__()
        self.dumper = dumper
        self.selector = selector
        self.attributor = attributor

    # node/hierarchy interface
    @retries_when(TransportDisconnected, delay=3.0)
    @transform_node_has_been_removed_exception
    def getAttr(self, nodes, name):
        return self.attributor.getAttr(nodes, name)

    @retries_when(TransportDisconnected, delay=3.0)
    @transform_node_has_been_removed_exception
    def setAttr(self, nodes, name, value):
        return self.attributor.setAttr(nodes, name, value)

    @retries_when(TransportDisconnected, delay=3.0)
    def select(self, query, multiple=False):
        return self.selector.select(query, multiple)

    @retries_when(TransportDisconnected, delay=3.0)
    def dump(self):
        return self.dumper.dumpHierarchy()
