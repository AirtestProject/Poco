# coding=utf-8
from .DefaultMatcher import DefaultMatcher
from .exceptions import NoSuchTargetException

__author__ = 'lxn3032'
__all__ = ['ISelector', 'Selector']


class ISelector(object):
    """
    This interface defines standard selector behavior. Selector is used for selecting specific UI element by given query 
    condition (formal definitions are in specific implementation classes).
    """

    def select(self, cond, multiple=False):
        """
        Args:
            cond (:obj:`tuple`): query conditions.
            multiple (:obj:`bool`): Whether or not to select element multiple. This method returns once a node found if 
             multiple is True, returns after traversing through all nodes otherwise.

        Returns:
            :obj:`list` <inherit from :py:class:`AbstractNode <poco.sdk.AbstractNode>`> : 
        """

        raise NotImplementedError


class Selector(ISelector):
    """
    This class implements standard Selector interface that uses BFS algorithm to travers through tree-like hierarchy 
    structure. It supports flexible query conditions such as parental relationship, attribute predicate and etc. Any 
    combinations of expressions are also an query conditions.
    
    The query condition (query expression) defines as following::

        expr := (op0, (expr0, expr1))
        expr := ('index', (expr, :obj:`int`))
        expr := <other query condition> See implementation of Matcher.

    - ``op0`` can be one of the following ('>', '/', '-'), each operator stands for as follows::

        '>': offsprings, to select all offsprings matched expr1 from all roots matched expr0.
        '/': children, to select all children matched expr1 from all roots matched expr0.
        '-': siblings, to select all siblings matched expr1 from all roots matched expr0.
    
    - ``'index'``: to select specific nth UI element from previous results.

    - ``others``: will pass expression to matcher.

    Args:
        dumper (any implements :py:class:`IDumper <poco.sdk.AbstractDumper.IDumper>`): The dumper for selector.
        matcher (any implements :py:class:`IMatcher <poco.sdk.DefaultMatcher.IMatcher>`): :py:class:`DefaultMatcher \
         <poco.sdk.DefaultMatcher.DefaultMatcher>` instance by default.
    """

    def __init__(self, dumper, matcher=None):
        self.dumper = dumper
        self.matcher = matcher or DefaultMatcher()

    def getRoot(self):
        """
        Get a default root node.

        Returns:
            Default root node from dumper. 
        """

        return self.dumper.getRoot()

    def select(self, cond, multiple=False):
        """
        See Also: :py:meth:`select <poco.sdk.Selector.ISelector.select>` method in ``ISelector``.
        """

        return self.selectImpl(cond, multiple, self.getRoot(), 9999, True, True)

    def selectImpl(self, cond, multiple, root, maxDepth, onlyVisibleNode, includeRoot):
        """
        Selector internal implementation. 
        TODO: add later.

        .. note:: This doc string only shows the outline of the algorithm. Do not call this method in your code as this 
         is a internal impl method.

        Args:
            cond (:obj:`tuple`): Query condition.
            multiple (:obj:`bool`): Whether or not only select the first matched Node.
            root (inherit from :py:class:`AbstractNode <poco.sdk.AbstractNode>`): Start traversing from the given root.
            maxDepth (:obj:`bool`): Max traversing depth.
            onlyVisibleNode (:obj:`bool`): If True, skip the Node whose visibility (the value of visible attribute) is 
             False.
            includeRoot (:obj:`bool`): Whether not not include the root node if its child node matched.

        Returns:
            :obj:`list` <inherit from :py:class:`AbstractNode <poco.sdk.AbstractNode>`>: The same as \
             :py:meth:`select <poco.sdk.Selector.ISelector.select>`.
        """

        result = []
        if not root:
            return result

        op, args = cond

        if op in ('>', '/'):
            # children or offsprings
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
            # sibling
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
        # exclude invisible UI element if onlyVisibleNode specified
        # 剪掉不可见节点branch
        if onlyVisibleNode and not node.getAttr('visible'):
            return False

        if self.matcher.match(cond, node):
            # To select node from parent or ancestor, the parent or ancestor are excluded.
            # 父子/祖先后代节点选择时，默认是不包含父节点/祖先节点的
            # 在下面的children循环中则需要包含，因为每个child在_selectTraverse中就当做是root
            if includeRoot:
                outResult.append(node)
                if not multiple:
                    return True

        # When maximum search depth reached, children of this node is still require to travers.
        # 最大搜索深度耗尽并不表示遍历结束，其余child节点仍需遍历
        if maxDepth == 0:
            return False
        maxDepth -= 1

        for child in node.getChildren():
            finished = self._selectTraverse(cond, child, outResult, multiple, maxDepth, onlyVisibleNode, True)
            if finished:
                return True

        return False
