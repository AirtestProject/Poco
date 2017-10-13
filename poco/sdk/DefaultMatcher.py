# coding=utf-8

import re
from .exceptions import NoSuchComparatorException

__author__ = 'lxn3032'
__all__ = ['DefaultMatcher']


class IMatcher(object):
    def match(self, cond, node):
        """
        Test whether or not the node matches the given condition.

        :param cond: Query condition.
        :param node: Node instance inherited from `AbstractNode`.
        :rettype: bool
        :return: True if matches otherwise False.
        """

        raise NotImplementedError


class EqualizationComparator(object):
    """
    Compare two object using native equal (==) comparison.
    """

    def compare(self, l, r):
        return l == r


class RegexpComparator(object):
    """
    Compare two object using regular expression matching comparison. Available only when origin value is string. Result
    in False if origin value or given pattern is not string.
    """

    def compare(self, origin, pattern):
        if origin is None or pattern is None:
            return False
        return re.match(pattern, origin) is not None


class DefaultMatcher(IMatcher):
    """
    Default matcher implementation for poco hierarchy traversing.
    """

    def __init__(self):
        super(DefaultMatcher, self).__init__()
        self.comparators = {
            'attr=': EqualizationComparator(),
            'attr.*=': RegexpComparator(),
        }

    def match(self, cond, node):
        op, args = cond

        # 条件匹配
        if op == 'and':
            for arg in args:
                if not self.match(arg, node):
                    return False
            return True

        if op == 'or':
            for arg in args:
                if self.match(arg, node):
                    return True
            return False

        # 属性匹配
        comparator = self.comparators.get(op)
        if comparator:
            attribute, value = args
            targetValue = node.getAttr(attribute)
            return comparator.compare(targetValue, value)

        raise NoSuchComparatorException(op, 'support.poco.sdk.DefaultMatcher')
