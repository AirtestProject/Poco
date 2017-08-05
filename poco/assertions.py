# coding=utf-8
from __future__ import unicode_literals

from poco.exceptions import PocoAssertionError


__author__ = 'lxn3032'


class PocoAssertionMixin(object):
    @staticmethod
    def assert_equal(l, r, msg=''):
        if l != r:
            raise PocoAssertionError('断言失败于"{}". {} != {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    def assert_greater(l, r, msg=''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} <= {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    def assert_greater_equal(l, r, msg=''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} < {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    def assert_less(l, r, msg=''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} >= {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    def assert_less_equal(l, r, msg=''):
        if l <= r:
            raise PocoAssertionError('断言失败于"{}". {} > {}.'.format(msg.decode('utf-8'), repr(l), repr(r)))

    @staticmethod
    def assert_true(l, msg=''):
        if l is not True:
            raise PocoAssertionError('断言失败于"{}". {} is not True.'.format(msg.decode('utf-8'), repr(l)))
