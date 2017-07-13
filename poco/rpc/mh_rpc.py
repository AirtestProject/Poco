# -*- coding: utf-8 -*-
# @Author: gzliuxin
# @Email:  gzliuxin@corp.netease.com
# @Date:   2017-07-13 18:01:23
import sys
sys.path.append(r"D:\dev\snippet\tcpserver")

from . import RpcInterface, RpcRemoteException, RpcTimeoutException
from rpcclient import RpcClient as AsyncRpc
from rpcclient import AsyncConn
from functools import wraps


def sync_wrapper(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        cb = func(*args, **kwargs)
        ret, err = cb.wait()
        if err:
            raise RpcRemoteException(err)
        return ret
    return new_func


class MhRpc(RpcInterface):
    """docstring for MhRpc"""

    def __init__(self):
        super(MhRpc, self).__init__()
        conn = AsyncConn(("localhost", 5001))
        self.c = AsyncRpc(conn)
        self.c.run(backend=True)

    @sync_wrapper
    def get_screen_size(self):
        return self.c.call("get_size")

    @sync_wrapper
    def dump(self):
        return self.c.call("dump")

    def select(self, query, multiple=False):
        dump = self.dump()
        root = dict_2_node(dump)
        print(query)

        nodes = self._select(query, root=root)
        return nodes

    def make_selection(self, node):
        return [node]

    def getattr(self, nodes, name):
        node = nodes[0]
        return node.getAttr(name)

    def setattr(self, nodes, name, val):
        node_id = nodes[0]["desc"]
        self._setattr(node_id, name, val)

    @sync_wrapper
    def _setattr(self, node_id, name, val):
        return self.c.call("setattr", node_id, name, val)

    @sync_wrapper
    def click(self, pos):
        return self.c.call("click", pos)

    @classmethod
    def _select(cls, cond, multiple=True, root=None, matcher=None, max_depth=99999, onlyVisibleNode=True, includeRoot=True):
        """
        凡是visible为False后者parentVisible为false的都不选
        """
        # root = root or cls.root()
        matcher = matcher or cls._defaultMatcher
        result = []

        op, args = cond

        if op in ('>', '/'):
            # 父子直系相对节点选择
            parents = [root]
            for index, arg in enumerate(args):
                midResult = []
                for parent in parents:
                    if op == '/' and index != 0:
                        _max_depth = 1
                    else:
                        _max_depth = max_depth
                    # 按路径进行遍历一定要multiple为true才不会漏掉
                    _res = cls._select(arg, True, parent, matcher, _max_depth, onlyVisibleNode, False)
                    midResult += _res
                parents = midResult
            result = parents
        elif op == '-':
            # 兄弟节点选择
            query1, query2 = args
            result1 = cls._select(query1, multiple, root, matcher, max_depth, onlyVisibleNode, includeRoot)
            for n in result1:
                result += cls._select(query2, multiple, n.getParent(), matcher, 1, onlyVisibleNode, includeRoot)
        elif op == 'index':
            cond, i = args
            try:
                result = [cls._select(cond, multiple, root, matcher, max_depth, onlyVisibleNode, includeRoot)[i]]
            except IndexError:
                raise RpcRemoteException(u'Query results index out of range. Index={} condition "{}" from root "{}".'.format(i, cond, cls.root()))
        else:
            cls._selectTraverse(cond, root, matcher, result, multiple, max_depth, onlyVisibleNode, includeRoot)

        return result

    @classmethod
    def make_selection(cls, obj):
        # 仅仅用list包一下，为了让poco那边能直接生成一个select的结果
        return [obj]

    @classmethod
    def _selectTraverse(cls, cond, node, matcher, outResult, multiple, max_depth, onlyVisibleNode, includeRoot):
        # 剪掉不可见节点branch
        if onlyVisibleNode and not node.isVisible():
            return

        if matcher(cond, node):
            # 父子/祖先后代节点选择时，默认是不包含父节点/祖先节点的
            # 在下面的children循环中则需要包含，因为每个child在_selectTraverse中就当做是root
            if includeRoot:
                outResult.append(node)
                if not multiple:
                    return True

        # 最大搜索深度耗尽并不表示遍历结束，其余child节点仍需遍历
        if max_depth == 0:
            return
        max_depth -= 1

        children = node.getChildren()
        if children:
            for child in children:
                finished = cls._selectTraverse(cond, child, matcher, outResult, multiple, max_depth, onlyVisibleNode, True)
                if finished:
                    return True

    Predicates = {
        'attr=':  lambda l, r: l == r,
        'attr.*=': lambda origin, pattern: re.match(pattern, origin) is not None,
    }

    @classmethod
    def _defaultMatcher(cls, cond, node):
        op, args = cond

        # 条件选择
        if op == 'or':
            matched = False
            for arg in args:
                matched = matched or cls._defaultMatcher(arg, node)
                if matched:
                    break
            return matched

        if op == 'and':
            matched = True
            for arg in args:
                matched = matched and cls._defaultMatcher(arg, node)
                if not matched:
                    break
            return matched

        # 属性选择
        if op in cls.Predicates:
            pred = cls.Predicates.get(op)
            attribute, value = args
            attrVal = node.getAttr(attribute, None)
            return pred(attrVal, value)

        return False


class Node(object):
    """Node Implimentation of Dict"""

    def __init__(self, data, parent=None):
        self.data = data.get("payload", {})
        self.parent = parent
        self.children = []

    def getAttr(self, name, default=None):
        if name == "screenPosition":
            name = "pos"
        elif name == "anchorPosition":
            x, y = self.data.get("pos")
            w, h = self.data.get("size")
            return (x + w / 2, y + h / 2)
        v = self.data.get(name, default)
        return v

    def getParent(self):
        return self.parent

    def getChildren(self):
        return self.children

    def isVisible(self):
        return True


def dict_2_node(data, parent=None):
    children = data.pop("children", None)
    node = Node(data, parent)
    if children:
        for c in children:
            c_node = dict_2_node(c, node)
            node.children.append(c_node)
    return node


if __name__ == '__main__':
    from pprint import pprint
    r = MhRpc()
    size = r.get_screen_size()
    r.click((0.5, 0.5))
    # dump = r.dump()
    # pprint(dump)
    # root = (dict_2_node(dump))
    # pprint(root)
    # pprint(root.getParent())
    # pprint(root.getChildren())
    # nodes = r.select(["and",[["attr=",["text",u"手机也能玩"]]]])
    # nodes = r.select(["and",[["attr=",["type", "Text"]]]])
    # pprint(nodes)
