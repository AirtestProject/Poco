# coding=utf-8
from __future__ import unicode_literals

from poco.exceptions import PocoAssertionError
from poco.utils.suppression import deprecated


__author__ = 'lxn3032'


# deprecated, use assertion method in pocounit.case.PocoTestCase instead
class PocoAssertionMixin(object):
    """
    Warnings:
        Deprecated, do not use! Use assertion method in ``pocounit.PocoTestCase`` instead.
    """

    @staticmethod
    @deprecated('use assertion method in pocounit.case.PocoTestCase instead')
    def assert_equal(l, r, msg=b''):
        if l != r:
            raise PocoAssertionError('断言失败于"{}". {} != {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    @deprecated('use assertion method in pocounit.case.PocoTestCase instead')
    def assert_greater(l, r, msg=b''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} <= {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    @deprecated('use assertion method in pocounit.case.PocoTestCase instead')
    def assert_greater_equal(l, r, msg=b''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} < {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    @deprecated('use assertion method in pocounit.case.PocoTestCase instead')
    def assert_less(l, r, msg=b''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} >= {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    @deprecated('use assertion method in pocounit.case.PocoTestCase instead')
    def assert_less_equal(l, r, msg=b''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} > {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    @deprecated('use assertion method in pocounit.case.PocoTestCase instead')
    def assert_true(l, msg=b''):
        if l is not True:
            raise PocoAssertionError('断言失败于"{}". {} is not True.'.format(msg.decode('utf-8'), repr(l)))
