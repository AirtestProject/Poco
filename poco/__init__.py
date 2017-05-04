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
        """
        实例化一个poco对象，一般每个testcase都实例化一个。

        :param hunter:  hunter对象，通过hunter_cli.Hunter构造
        :param kwargs:
            action_interval: 操作间隙，主要为点击操作之后要等待的一个间隙时间，默认1s
            poll_interval: 轮询间隔，通过轮询等待某个事件发生时的一个时间间隔，如每poll_interval秒判断一次某按钮是否出现或消失
        """
        super(PocoUI, self).__init__()
        self.hunter = hunter
        self.rpc_client = HunterRpcClient(hunter)
        self.remote_poco = self.rpc_client.remote('poco-uiautomation-framework')
        self.selector = self.remote_poco.selector
        self.screen_resolution = self.remote_poco.get_screen_size()

        # options
        self._post_action_interval = kwargs.get('action_interval', 1)
        self._poll_interval = kwargs.get('poll_interval', 3)

    def __call__(self, name=None, **kw):
        """
        选择ui对象或对象集合。可通过节点名和其余节点属性共同选择。例如 poco('close', type='Button')
        总是选择可见的节点，不可见的已自动过滤
        节点名与节点属性值由具体ui框架定义。

        :param name: ui节点名，默认None则不通过name进行选择
        :param kw:
            ui其他属性选择器
            type: 节点类型，Button、Sprite、Node等,
            text: 节点文本值，比如按钮上面的字之类的,
            enable: 是否使能，True/False,
            touchenable: 是否可点击，True/False,
            textNot: 文本不等于，选出文本值不为xxx的节点,
            typeNot: 类型不等于，选出类型不为xxx的节点,
        :return: UI代理对象
        """
        return UIObjectProxy(self, name, **kw)

    def wait_for_any(self, objects, timeout=120):
        """
        等待任一对象出现，对给定objects中的每个对象依次轮询，直到某个对象出现（可见），并返回该对象

        :param objects: 等待的目标的集合
        :param timeout: 最长等待时间
        :return: 等到的那个对象
        """
        start = time.time()
        while True:
            for obj in objects:
                if obj.exists():
                    return obj
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to appear'.format(objects))
            self.sleep_for_polling_interval()

    def wait_for_all(self, objects, timeout=120):
        """
        等待所有给定对象出现，对给定objects中的每个对象依次轮询，直到所有对象都出现

        :param objects: 等待的目标的集合
        :param timeout: 最长等待时间
        :return: None
        """
        start = time.time()
        while True:
            all_exist = True
            for obj in objects:
                if not obj.exists():
                    all_exist = False
                    break
            if all_exist:
                return
            if time.time() - start > timeout:
                raise RuntimeError('Timeout at waiting for {} to appear'.format(objects))
            self.sleep_for_polling_interval()

    def wait_stable(self):
        time.sleep(self._post_action_interval)

    def sleep_for_polling_interval(self):
        time.sleep(self._poll_interval)

    def command(self, script, lang='text'):
        """
        通过hunter调用gm指令，可调用hunter指令库中定义的所有指令，也可以调用text类型的gm指令
        gm指令相关功能请参考safaia GM指令扩展模块

        :param script: 指令
        :param lang: 语言，默认text
        :return: None
        """
        self.hunter.script(script, lang=lang)
        self.wait_stable()

    # input interface
    def touch(self, pos):
        if not (0 <= pos[0] <= self.screen_resolution[0]) or not (0 <= pos[1] <= self.screen_resolution[1]):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))

    def swipe(self, p1, p2=None, direction=None, duration=0.5):
        if not (0 <= p1[0] <= self.screen_resolution[0]) or not (0 <= p1[1] <= self.screen_resolution[1]):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))

    def long_click(self, pos, duration=2):
        if not (0 <= pos[0] <= self.screen_resolution[0]) or not (0 <= pos[1] <= self.screen_resolution[1]):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
