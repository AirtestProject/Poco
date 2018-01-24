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
            cond (:obj:`tuple`): query expression
            node (:py:class:`inherit from AbstractNode <poco.sdk.AbstractNode>`): node to be tested

        Returns:
            bool: True if matches otherwise False.
        """

        raise NotImplementedError


class EqualizationComparator(object):
    """
    Compare two objects using the native equivalence (==) comparison operator
    """

    def compare(self, l, r):
        return l == r


class RegexpComparator(object):
    """
    Compare two objects using regular expression. Available only when the original value is string type. It always
    returns False if the original value or given pattern are not :obj:`str` type.
    """

    def compare(self, origin, pattern):
        """
        Args:
            origin (:obj:`str`): original string
            pattern (:obj:`str`): Regexp pattern string

        Returns:
            bool: True if matches otherwise False.
        """

        if origin is None or pattern is None:
            return False
        return re.match(pattern, origin) is not None


class DefaultMatcher(IMatcher):
    """
    Default matcher implementation for poco hierarchy traversing. Including logical query condition and predicate
    expression. When traversing through the hierarchy tree, matcher will apply the match method on each node of the tree.

    The formal definition of query condition as follows::

        expr := (op0, (expr0, expr1, ...))  
        expr := (op1, (arg1, arg2))  

    - ``op0``:obj:`str` is logical operator ('or' or 'and') which has the same semantics as in python, e.g. 'or'
      means this expression/condition matches if any of the exprN matches
    - ``op1``:obj:`str` is comparator, can be one of as follows::

        op1 := 'attr='
        op1 := 'attr.*='
        op1 := ... (other customized)

      - ``attr=`` corresponds to :py:class:`EqualizationComparator <poco.sdk.DefaultMatcher.EqualizationComparator>`.
      - ``attr.*=`` corresponds to :py:class:`RegexpComparator <poco.sdk.DefaultMatcher.RegexpComparator>`.
      
      The ``op1`` must be a string. The ``Matcher`` will help to map to ``Comparator`` object.
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
