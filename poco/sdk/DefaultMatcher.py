# coding=utf-8

import re
import sys

from poco.sdk.IMatcher import IMatcher

from .exceptions import NoSuchComparatorException

__author__ = 'lxn3032'
__all__ = ['DefaultMatcher']
PY2 = sys.version_info[0] == 2


class EqualizationComparator(object):
    def compare(self, l, r):
        return l == r


class RegexpComparator(object):
    def compare(self, origin, pattern):
        if origin is None or pattern is None:
            return False
        if PY2 and isinstance(origin, str):
            origin = origin.decode('utf-8')  # 如果游戏是gbk编码的话，那就要实现AbstractNode时就把编码转好，不要走到这里才转
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
