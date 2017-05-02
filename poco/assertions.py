# coding=utf-8
__author__ = 'lxn3032'


class PocoUIAssertionMixin(object):
    @staticmethod
    def assert_equal(l, r, msg=''):
        if l != r:
            raise AssertionError('断言失败于"{}". {} != {}.'.format(msg, repr(l), repr(r)))

    @staticmethod
    def assert_greater(l, r, msg=''):
        if l <= r:
            raise AssertionError('断言失败于"{}". {} <= {}.'.format(msg, repr(l), repr(r)))

    @staticmethod
    def assert_greater_equal(l, r, msg=''):
        if l <= r:
            raise AssertionError('断言失败于"{}". {} < {}.'.format(msg, repr(l), repr(r)))

    @staticmethod
    def assert_less(l, r, msg=''):
        if l <= r:
            raise AssertionError('断言失败于"{}". {} >= {}.'.format(msg, repr(l), repr(r)))

    @staticmethod
    def assert_less_equal(l, r, msg=''):
        if l <= r:
            raise AssertionError('断言失败于"{}". {} > {}.'.format(msg, repr(l), repr(r)))

    @staticmethod
    def assert_true(l, msg=''):
        if l is not True:
            raise AssertionError('断言失败于"{}". {} is not True.'.format(msg, repr(l)))
