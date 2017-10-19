# coding=utf-8

import re
from .exceptions import NoSuchComparatorException

__author__ = 'lxn3032'
__all__ = ['IMatcher', 'DefaultMatcher', 'EqualizationComparator', 'RegexpComparator']


class IMatcher(object):
    def match(self, cond, node):
        """
        Test whether or not the node matches the given condition.

        Args:
            cond (:obj:`tuple`): Query condition.
            node (:py:class:`inherit from AbstractNode <poco.sdk.AbstractNode>`): Node to be tested.

        Returns:
            bool: True if matches otherwise False.
        """

        raise NotImplementedError


class EqualizationComparator(object):
    """
    Compare two object using native equivalence (==) comparison.
    """

    def compare(self, l, r):
        return l == r


class RegexpComparator(object):
    """
    Compare two object using regular expression matching comparison. Available only when origin value is string. Result
    in False if origin value or given pattern is not :obj:`str`.
    """

    def compare(self, origin, pattern):
        """
        Args:
            origin (:obj:`str`): Origin string.
            pattern (:obj:`str`): Regexp pattern string.

        Returns:
            bool: True if matches otherwise False.
        """

        if origin is None or pattern is None:
            return False
        return re.match(pattern, origin) is not None


class DefaultMatcher(IMatcher):
    """
    Default matcher implementation for poco hierarchy traversing. Including logical query condition and predicate  
    expression. When traversing through the hierarchy tree, matcher will apply match method on each tree node.

    The formal definition of query condition as follows::

        expr := (op0, (expr0, expr1, ...))  
        expr := (op1, (arg1, arg2))  

    - ``op0``:obj:`str` is logical operator ('or' or 'and') which has the same semantics as in python. e.g. 'or' 
      means this expression/condition matches if any of the exprN matches.
    - ``op1``:obj:`str` is comparator, can be one of as follows::

        op1 := 'attr='
        op1 := 'attr.*='
        op1 := ... (other customized)

      - ``attr=`` corresponds to :py:class:`EqualizationComparator <poco.sdk.DefaultMatcher.EqualizationComparator>`.
      - ``attr.*=`` corresponds to :py:class:`RegexpComparator <poco.sdk.DefaultMatcher.RegexpComparator>`.
      
      The ``op1`` is only a string. ``Matcher`` will help to map to ``Comparator`` object.
    """

    def __init__(self):
        super(DefaultMatcher, self).__init__()
        self.comparators = {
            'attr=': EqualizationComparator(),
            'attr.*=': RegexpComparator(),
        }

    def match(self, cond, node):
        """
        See Also: :py:meth:`IMatcher.match <poco.sdk.DefaultMatcher.IMatcher.match>`
        """

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

        raise NoSuchComparatorException(op, 'poco.sdk.DefaultMatcher')
