# coding=utf-8

__author__ = 'lxn3032'
__all__ = ['AbstractNode']


class AbstractNode(object):
    RequiredAttributes = (
        "name",
        "type",
        "visible",
        "pos",
        "size",
        "scale",
        "anchorPoint",
        "zOrders",
    )

    def getParent(self):
        """
        :rettype: AbstractNode
        """

        raise NotImplementedError

    def getChildren(self):
        """
        :rettype: Iterable<AbstractNode>
        """

        raise NotImplementedError

    def getAttr(self, attrName):
        """
        :rettype: <any>
        """

        raise NotImplementedError

    def setAttr(self, attrName, val):
        """
        :retval: None
        """

        raise NotImplementedError

    def enumerateAttrs(self):
        """
        :rettype: Iterable<string, ValueType>
        """

        raise NotImplementedError
