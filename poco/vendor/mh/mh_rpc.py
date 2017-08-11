# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-13 18:01:23
from functools import wraps

from poco.sdk.Dumpable import Dumpable
from poco.interfaces.screen import ScreenInterface
from poco.interfaces.input import InputInterface
from poco.vendor.legacy_mode.hierarchy import LegacyModeHierarchy




def sync_wrapper(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        cb = func(*args, **kwargs)
        ret, err = cb.wait()
        if err:
            raise err
        return ret
    return new_func


class MhScreen(ScreenInterface):
    def __init__(self, client):
        super(MhScreen, self).__init__()
        self.c = client

    @sync_wrapper
    def get_screen_size(self):
        return self.c.call("get_size")

    @sync_wrapper
    def snapshot(self, width):
        return self.c.call("get_size")


class MhInput(InputInterface):
    def __init__(self, client):
        super(MhInput, self).__init__()
        self.c = client

    @sync_wrapper
    def click(self, pos, op="left"):
        print(pos, op)
        return self.c.call("click", pos, op)


class MhDumper(Dumpable):
    def __init__(self, client):
        super(MhDumper, self).__init__()
        self.c = client

    @sync_wrapper
    def dumpHierarchy(self):
        return self.c.call("dump")


class MhHierarchy(LegacyModeHierarchy):
    def __init__(self, client):
        super(MhHierarchy, self).__init__(MhDumper(client))
        self.c = client

    def setattr(self, node, name, val):
        if isinstance(node, (list, tuple)):
            node = node[0]
        node_id = node[0]["desc"]
        self._setattr(node_id, name, val)

    @sync_wrapper
    def _setattr(self, node_id, name, val):
        return self.c.call("setattr", node_id, name, val)


# class MhRpc(RpcInterface):
#     """docstring for MhRpc"""
#
#     def __init__(self, addr=("localhost", 5001)):
#         super(MhRpc, self).__init__(uihierarchy=LegacyModeHierarchy(self.dump))
#         conn = AsyncConn(addr)
#         self.c = RpcClient(conn)
#         self.c.run(backend=True)
#
#     @sync_wrapper
#     def get_screen_size(self):
#         return self.c.call("get_size")
#
#     @sync_wrapper
#     def get_screen(self, width):
#         return self.c.call("get_screen")
#
#     @sync_wrapper
#     def dump(self):
#         return self.c.call("dump")
#
#     def setattr(self, node, name, val):
#         if isinstance(node, (list, tuple)):
#             node = node[0]
#         node_id = node[0]["desc"]
#         self._setattr(node_id, name, val)
#
#     @sync_wrapper
#     def _setattr(self, node_id, name, val):
#         return self.c.call("setattr", node_id, name, val)
#
#     @sync_wrapper
#     def click(self, pos, op="left"):
#         print(pos, op)
#         return self.c.call("click", pos, op)


if __name__ == '__main__':
    from pprint import pprint
    r = MhRpc(addr=("10.254.245.124", 5001))
    # size = r.get_screen_size()
    # r.click((0.5, 0.5))
    # dump = r.dump()
    # pprint(dump)
    # root = (dict_2_node(dump))
    # pprint(root)
    # pprint(root.getParent())
    # pprint(root.getChildren())
    nodes = r.select(["and",[["attr=",["text", u"长安城"]]]])
    # nodes = r.select(["and",[["attr=",["type", "Text"]]]])
    pprint(nodes[0].node)
