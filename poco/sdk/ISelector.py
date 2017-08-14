# coding=utf-8

class ISelector(object):
    def select(self, cond, multiple=False):
        """
        :rettype: list of support.poco.sdk.AbstractNode
        """

        raise NotImplementedError