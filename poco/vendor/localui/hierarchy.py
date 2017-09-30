# coding=utf-8 
from poco.sdk.AbstractDumper import AbstractDumper
from poco.sdk.AbstractNode import AbstractNode
from poco.sdk.Attributor import Attributor
from poco.sdk.Selector import Selector
from poco.sdk.exceptions import UnableToSetAttributeException
from poco.sdk.interfaces.hierarchy import HierarchyInterface


class LocalUIHierarchy(HierarchyInterface):
    """local implementation of UIInterface
        `dump` of dumper is the only method to be implemented
    """
    def __init__(self, dumper):
        super(LocalUIHierarchy, self).__init__()
        self.dumper = dumper
        self.selector = Selector(self.dumper)
        self.attributor = Attributor()

    def dump(self):
        return self.dumper.dumpHierarchy()

    def getAttr(self, nodes, name):
        """get node attribute"""
        return self.attributor.getAttr(nodes, name)

    def setAttr(self, nodes, name, value):
        """set node attribute"""
        return self.attributor.setAttr(nodes, name, value)

    def select(self, query, multiple=False):
        """select nodes by query"""
        return self.selector.select(query, multiple)


class Node(AbstractNode):
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

    def getAvailableAttributeNames(self):
        return super(Node, self).getAvailableAttributeNames() + (
            'text',
            'touchable',
            'enabled',
            'tag',
            'desc',
            'rotation',
        )


class LocalUIDumper(AbstractDumper):

    def dumpHierarchy(self):
        raise NotImplementedError

    def getRoot(self):
        # 每次获取root时，就给一个新的root
        root = Node(self.dumpHierarchy())
        for child in root.getChildren():
            child.setParent(root)
        return root
