# coding=utf-8


from poco.sdk.AbstractNode import AbstractNode
from poco.sdk.exceptions import UnableToSetAttributeException


__author__ = 'lxn3032'
__all__ = ['Node']


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
        for child in self.node.get('children', []):
            yield Node(child)

    def getAttr(self, attrName):
        return self.node['payload'].get(attrName)

    def setAttr(self, attrName, val):
        # cannot set any attributes on local nodes
        raise UnableToSetAttributeException(attrName, self.node)

    def enumerateAttrs(self):
        for attrName in self.RequiredAttributes + self.SecondaryAttributes:
            yield attrName, self.getAttr(attrName)
