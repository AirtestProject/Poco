# coding=utf-8
__author__ = 'lxn3032'


import time
from hunter_cli.rpc.client import HunterRpcClient

from .input import InputInterface
from .proxy import UIObjectProxy
from .exceptions import InvalidOperationException
from .assertions import PocoUIAssertionMixin
from .acceleration import PocoUIAccelerationMixin


class PocoUI(InputInterface, PocoUIAssertionMixin, PocoUIAccelerationMixin):
    def __init__(self, hunter, **kwargs):
        super(PocoUI, self).__init__()
        self.hunter = hunter
        self.rpc_client = HunterRpcClient(hunter)
        self.remote_poco = self.rpc_client.remote('poco-uiautomation-framework')
        self.selector = self.remote_poco.selector
        self.screen_size = self.remote_poco.get_screen_size()

        # options
        self._post_action_interval = kwargs.get('action_interval', 1)
        self._poll_interval = kwargs.get('poll_interval', 3)

    def __call__(self, name=None, **kw):
        return UIObjectProxy(self, name, **kw)

    def wait_for_any(self, objects, timeout=120):
        start = time.time()
        while True:
            for obj in objects:
                if obj.exists():
                    return obj
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to appear'.format(objects))
            self.sleep_for_polling_interval()

    def wait_for_all(self, *objects, **kw):
        pass

    def wait_stable(self):
        time.sleep(self._post_action_interval)

    def sleep_for_polling_interval(self):
        time.sleep(self._poll_interval)

    def command(self, script, lang='text'):
        self.hunter.script(script, lang=lang)
        self.wait_stable()

    # input interface
    def touch(self, pos):
        if not (0 <= pos[0] <= self.screen_size[0]) or not (0 <= pos[1] <= self.screen_size[1]):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))

    def swipe(self, p1, p2=None, direction=None, duration=0.5):
        if not (0 <= p1[0] <= self.screen_size[0]) or not (0 <= p1[1] <= self.screen_size[1]):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))

    def long_click(self, pos, duration=2):
        if not (0 <= pos[0] <= self.screen_size[0]) or not (0 <= pos[1] <= self.screen_size[1]):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
