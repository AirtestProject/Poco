# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['Attributor']


class Attributor(object):
    """
    This is a helper class to access node's attribute. In some cases it is not able to explicitly invoke node's member  
    function thus the following 2 functions are introduced.
    The instance of this class will be used in implementation of `HierarchyInterface`.
    """

    def getAttr(self, node, attrName):
        if type(node) in (list, tuple):
            node = node[0]
        return node.getAttr(attrName)

    def setAttr(self, node, attrName, attrVal):
        if type(node) in (list, tuple):
            node = node[0]
        node.setAttr(attrName, attrVal)
