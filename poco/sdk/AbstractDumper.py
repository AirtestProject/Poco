# coding=utf-8

from poco.sdk.IDumper import IDumper


__author__ = 'lxn3032'
__all__ = ['AbstractDumper']


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
