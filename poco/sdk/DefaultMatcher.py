# coding=utf-8

import re

from .exceptions import NoSuchComparatorException


__author__ = 'lxn3032'
__all__ = ['DefaultMatcher']


class IMatcher(object):
    def match(self, cond, node):
        """
        :rettype: bool
        """

        raise NotImplementedError


class EqualizationComparator(object):
    def compare(self, l, r):
        return l == r


class RegexpComparator(object):
    def compare(self, origin, pattern):
        if origin is None or pattern is None:
            return False
        return re.match(pattern, origin) is not None


class DefaultMatcher(IMatcher):
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
