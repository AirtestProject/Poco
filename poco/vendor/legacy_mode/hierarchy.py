# coding=utf-8 
from poco.interfaces.hierarchy import HierarchyInterface
from poco.sdk.Selector import Selector

from poco.sdk.AbstractDumper import AbstractDumper
from poco.sdk.AbstractNode import AbstractNode
from poco.sdk.Attributor import Attributor
from poco.sdk.exceptions import UnableToSetAttributeException


class LegacyModeHierarchy(HierarchyInterface):
    """local implementation of UIInterface
        `dumpHierarchy` is the only method to be implemented
    """
    def __init__(self, dumpable):
        super(LegacyModeHierarchy, self).__init__()
        self.dumper = Dumper(dumpable)
        self.selector = Selector(self.dumper)
        self.attributor = Attributor()

    def dump(self):
        return self.dumper.dumpHierarchy()

    def getattr(self, nodes, name):
        """get node attribute"""
        return self.attributor.getAttr(nodes, name)

    def setattr(self, nodes, name, value):
        """set node attribute"""
        # return self.attributor.setAttr(nodes, name, value)
        raise NotImplementedError

    def select(self, query, multiple=False):
        """select nodes by query"""
        return self.selector.select(query, multiple)


class Node(AbstractNode):
    SecondaryAttributes = (
        'text',
        'touchable',
        'enabled',
        'tag',
        'desc',
        'rotation',
    )

    def __init__(self, node):
        super(Node, self).__init__()
        self.node = node

    def setParent(self, p):
        self.node['__parent__'] = p

    def getParent(self):
        return self.node.get('__parent__')

    def getChildren(self):
        for child in self.node.get('children') or []:
            yield Node(child)

    def getAttr(self, attrName):
        return self.node['payload'].get(attrName)

    def setAttr(self, attrName, val):
        # cannot set any attributes on local nodes
        raise UnableToSetAttributeException(attrName, self.node)

    def enumerateAttrs(self):
        for attrName in self.RequiredAttributes + self.SecondaryAttributes:
            yield attrName, self.getAttr(attrName)


class Dumper(AbstractDumper):
    def __init__(self, dumpable):
        self.dumpable = dumpable

    def _build_tree(self, root):
        for child in root.getChildren():
            child.setParent(root)
            self._build_tree(child)

    def getRoot(self):
        # 每次获取root时，就给一个新的root
        root = Node(self.dumpable.dumpHierarchy())
        for child in root.getChildren():
            child.setParent(root)
        return root

    def getPortSize(self):
        return 1.0, 1.0
