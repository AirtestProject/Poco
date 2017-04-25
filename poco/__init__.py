# coding=utf-8
__author__ = 'lxn3032'


import time
from hunter_cli.rpc.client import HunterRpcClient

from poco.input import InputInterface
from poco.proxy import UIObjectProxy


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


class PocoUI(InputInterface, PocoUIAssertionMixin):
    def __init__(self, hunter, **kwargs):
        super(PocoUI, self).__init__()
        self.hunter = hunter
        self.rpc_client = HunterRpcClient(hunter)
        self.remote_poco = self.rpc_client.remote('poco-uiautomation-framework')
        self.selector = self.remote_poco.selector

        # options
        self._post_action_interval = kwargs.get('action_interval', 1)
        self._poll_interval = kwargs.get('poll_interval', 3)

    def __call__(self, name=None, **kw):
        return UIObjectProxy(self, name, **kw)

    def wait_stable(self):
        time.sleep(self._post_action_interval)

    def wait_for_polling_interval(self):
        time.sleep(self._poll_interval)

    def command(self, script, lang='text'):
        self.hunter.script(script, lang=lang)
        self.wait_stable()

    def hide(self, uiobj):
        pass

    def show(self, uiobj):
        pass
