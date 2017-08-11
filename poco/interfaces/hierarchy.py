# coding=utf-8


class HierarchyInterface(object):

    def select(self, query, multiple):
        """
        在UI Hierarchy中根据query选取对象

        :param query: string built by poco
        :return: [list of nodes]
        """
        raise NotImplementedError

    def dump(self):
        """
        UI Hierarchy的JSON序列
        :return: json
        """
        raise NotImplementedError

    def getattr(self, nodes, name):
        """get node attribute"""
        raise NotImplementedError

    def setattr(self, nodes, name, value):
        """set node attribute"""
        raise NotImplementedError
