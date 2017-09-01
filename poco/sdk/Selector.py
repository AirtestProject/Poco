# coding=utf-8
from .DefaultMatcher import DefaultMatcher
from .exceptions import NoSuchTargetException

__author__ = 'lxn3032'
__all__ = ['Selector']


class ISelector(object):
    def select(self, cond, multiple=False):
        """
        :rettype: list of support.poco.sdk.AbstractNode
        """

        raise NotImplementedError


class Selector(ISelector):
    def __init__(self, dumper, matcher=None):
        self.dumper = dumper
        self.matcher = matcher or DefaultMatcher()

    def getRoot(self):
        return self.dumper.getRoot()

    def select(self, cond, multiple=False):
        return self.selectImpl(cond, multiple, self.getRoot(), 9999, True, True)

    def selectImpl(self, cond, multiple, root, maxDepth, onlyVisibleNode, includeRoot):
        """
        凡是visible为False后者parentVisible为false的都不选
        """

        result = []
        if not root:
            return result

        op, args = cond

        if op in ('>', '/'):
            # 父子直系相对节点选择
            parents = [root]
            for index, arg in enumerate(args):
                midResult = []
                for parent in parents:
                    if op == '/' and index != 0:
                        _maxDepth = 1
                    else:
                        _maxDepth = maxDepth
                    # 按路径进行遍历一定要multiple为true才不会漏掉
                    _res = self.selectImpl(arg, True, parent, _maxDepth, onlyVisibleNode, False)
                    midResult += _res
                parents = midResult
            result = parents
        elif op == '-':
            # 兄弟节点选择
            query1, query2 = args
            result1 = self.selectImpl(query1, multiple, root, maxDepth, onlyVisibleNode, includeRoot)
            for n in result1:
                result += self.selectImpl(query2, multiple, n.getParent(), 1, onlyVisibleNode, includeRoot)
        elif op == 'index':
            cond, i = args
            try:
                result = [self.selectImpl(cond, multiple, root, maxDepth, onlyVisibleNode, includeRoot)[i]]
            except IndexError:
                raise NoSuchTargetException(
                    u'Query results index out of range. Index={} condition "{}" from root "{}".'.format(i, cond, root))
        else:
            self._selectTraverse(cond, root, result, multiple, maxDepth, onlyVisibleNode, includeRoot)

        return result

    def _selectTraverse(self, cond, node, outResult, multiple, maxDepth, onlyVisibleNode, includeRoot):
        # 剪掉不可见节点branch
        if onlyVisibleNode and not node.getAttr('visible'):
            return False

        if self.matcher.match(cond, node):
            # 父子/祖先后代节点选择时，默认是不包含父节点/祖先节点的
            # 在下面的children循环中则需要包含，因为每个child在_selectTraverse中就当做是root
            if includeRoot:
                outResult.append(node)
                if not multiple:
                    return True

        # 最大搜索深度耗尽并不表示遍历结束，其余child节点仍需遍历
        if maxDepth == 0:
            return False
        maxDepth -= 1

        for child in node.getChildren():
            finished = self._selectTraverse(cond, child, outResult, multiple, maxDepth, onlyVisibleNode, True)
            if finished:
                return True

        return False
