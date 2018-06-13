# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['Attributor']


class Attributor(object):
    """
    This is a helper class to access the node attributes. In some cases it is not possible to explicitly invoke the
    node member functions thus the following two functions are introduced.

    The instance of this class will be used in implementation of :py:class:`HierarchyInterface \
    <poco.sdk.interfaces.hierarchy.HierarchyInterface>`.

    .. note:: Do not call these methods explicitly in the test codes.
    """

    def getAttr(self, node, attrName):
        if type(node) in (list, tuple):
            node_ = node[0]
        else:
            node_ = node
        return node_.getAttr(attrName)

    def setAttr(self, node, attrName, attrVal):
        if type(node) in (list, tuple):
            node_ = node[0]
        else:
            node_ = node
        node_.setAttr(attrName, attrVal)
