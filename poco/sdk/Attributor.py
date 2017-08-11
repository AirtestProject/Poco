# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['Attributor']


class Attributor(object):
    def getAttr(self, node, attrName):
        if type(node) in (list, tuple):
            node = node[0]
        return node.getAttr(attrName)

    def setAttr(self, node, attrName, attrVal):
        if type(node) in (list, tuple):
            node = node[0]
        node.setAttr(attrName, attrVal)
