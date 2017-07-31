# coding=utf-8
from __future__ import unicode_literals

import time
import warnings

from poco.interfaces.input import InputInterface
from poco.interfaces.screen import ScreenInterface

from .acceleration import PocoAccelerationMixin
from .assertions import PocoAssertionMixin
from .exceptions import PocoTargetTimeout
from .logging import HunterLoggingMixin
from .proxy import UIObjectProxy

__author__ = 'lxn3032'


class Poco(InputInterface, ScreenInterface, PocoAssertionMixin, PocoAccelerationMixin, HunterLoggingMixin):
    def __init__(self, rpc_client, **options):
        """
        实例化一个poco对象，一般每个testcase都实例化一个。

        :param hunter:  hunter对象，通过hunter_cli.Hunter构造
        :param options:
            action_interval: 操作间隙，主要为点击操作之后要等待的一个间隙时间，默认1s
            poll_interval: 轮询间隔，通过轮询等待某个事件发生时的一个时间间隔，如每poll_interval秒判断一次某按钮是否出现或消失
        """

        super(Poco, self).__init__()
        self._rpc_client = rpc_client

        # options
        self._pre_action_wait_for_appearance = options.get('pre_action_wait_for_appearance', 6)
        self._post_action_interval = options.get('action_interval', 0.5)
        self._poll_interval = options.get('poll_interval', 1.2)
        self._last_proxy = None

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
            touchable: 是否可点击，True/False,
            textMatches: 正则文本匹配,
            typeMatches: 正则类型名匹配,
        :return: UI代理对象
        """

        if not name and len(kw) == 0:
            warnings.warn("Wildcard selector may cause performance trouble. Please give at least one condition to "
                          "shrink range of results")
        self._last_proxy = UIObjectProxy(self, name, **kw)
        return self._last_proxy

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
                raise PocoTargetTimeout('any to appear', objects)
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
                raise PocoTargetTimeout('all to appear', objects)
            self.sleep_for_polling_interval()

    def wait_stable(self):
        time.sleep(self._post_action_interval)

    def sleep_for_polling_interval(self):
        time.sleep(self._poll_interval)

    @property
    def rpc(self):
        return self._rpc_client
