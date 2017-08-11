# coding=utf-8

from poco.sdk.Dumpable import Dumpable


__author__ = 'lxn3032'
__all__ = ['AbstractDumper']


class IDumper(Dumpable):
    def getRoot(self):
        """
        :rettype: support.poco.sdk.AbstractNode
        """

        raise NotImplementedError

    def dumpHierarchy(self):
        """
        :rettype: dict or NoneType
        """

        raise NotImplementedError

    def getPortSize(self):
        """
        hierarchy中的尺寸，一般就取屏幕的物理分辨率

        :retval:  [width, height] in floats of pixels
        :rettype: list
        """

        raise NotImplementedError


class AbstractDumper(IDumper):
    def dumpHierarchy(self):
        return self.dumpHierarchyImpl(self.getRoot())

    def dumpHierarchyImpl(self, node):
        if not node:
            return None

        payload = {}
        for attrName, attrVal in node.enumerateAttrs():
            if attrVal is not None:
                payload[attrName] = attrVal

        result = {}
        children = []
        for child in node.getChildren():
            if child.getAttr('visible'):
                children.append(self.dumpHierarchyImpl(child))
        if len(children) > 0:
            result['children'] = children

        result['name'] = node.getAttr('name')
        result['payload'] = payload

        return result
