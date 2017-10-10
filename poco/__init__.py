# coding=utf-8
from __future__ import unicode_literals

import time
import traceback
import warnings

from .acceleration import PocoAccelerationMixin
from .assertions import PocoAssertionMixin
from .exceptions import PocoTargetTimeout, InvalidOperationException
from .proxy import UIObjectProxy
from .agent import PocoAgent
from .freezeui.utils import create_immutable_hierarchy

__author__ = 'lxn3032'


class Poco(PocoAssertionMixin, PocoAccelerationMixin):
    def __init__(self, agent, **options):
        """
        Poco standard initializer.

        :param agent: a handler class object for poco to communication with target device. See `PocoAgent`'s definition.
        :param options:
            action_interval: The time after an action operated in order to wait for the UI becoming stable. default 0.8s.
            poll_interval: The minimum time between each poll event. Such as waiting for some UI to appear and it will 
                           be polling periodically.
            pre_action_wait_for_appearance: Before actions like click or swipe, it will wait for at most this time to 
                                            wait for appearance. If the target still not exists after that, 
                                            `PocoNoSuchNodeException` will raise
        """

        super(Poco, self).__init__()
        self._agent = agent

        # options
        self._pre_action_wait_for_appearance = options.get('pre_action_wait_for_appearance', 6)
        self._post_action_interval = options.get('action_interval', 0.8)
        self._poll_interval = options.get('poll_interval', 1.44)

        self._pre_action_callbacks = [self.on_pre_action.__func__]
        self._post_action_callbacks = [self.on_post_action.__func__]

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
                raise PocoTargetTimeout('any to appear', repr(objects).decode('utf-8'))
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
                raise PocoTargetTimeout('all to appear', repr(objects).decode('utf-8'))
            self.sleep_for_polling_interval()

    def freeze(this):
        class FreezedPoco(Poco):
            def __init__(self):
                hierarchy_dict = this.agent.hierarchy.dump()
                hierarchy = create_immutable_hierarchy(hierarchy_dict)
                agent_ = PocoAgent(hierarchy, this.agent.input, this.agent.screen)
                super(FreezedPoco, self).__init__(agent_, action_interval=0.01, pre_action_wait_for_appearance=0)
                self._pre_action_callbacks = this._pre_action_callbacks
                self._post_action_callbacks = this._post_action_callbacks

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        return FreezedPoco()

    def wait_stable(self):
        time.sleep(self._post_action_interval)

    def sleep_for_polling_interval(self):
        time.sleep(self._poll_interval)

    @property
    def agent(self):
        return self._agent

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(repr(pos).decode('utf-8')))
        self.agent.input.click(pos[0], pos[1])

    def swipe(self, p1, p2=None, direction=None, duration=2.0):
        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(repr(p1).decode('utf-8')))
        if direction is not None:
            p2 = [p1[0] + direction[0], p1[1] + direction[1]]
        elif p2 is not None:
            p2 = p2
        else:
            raise TypeError('Swipe end not set.')
        self.agent.input.swipe(p1[0], p1[1], p2[0], p2[1], duration)

    def long_click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(repr(pos).decode('utf-8')))
        self.agent.input.longClick(pos[0], pos[1])

    def snapshot(self, width=720):
        return self.agent.screen.getScreen(width)

    def get_screen_size(self):
        return self.agent.screen.getPortSize()

    def command(self, cmd, type=None):
        return self.agent.command.command(cmd, type)

    def on_pre_action(self, action, proxy, args):
        pass

    def on_post_action(self, action, proxy, args):
        pass

    def add_pre_action_callback(self, cb):
        self._pre_action_callbacks.append(cb)

    def add_post_action_callback(self, cb):
        self._post_action_callbacks.append(cb)

    def pre_action(self, action, proxy, args):
        for cb in self._pre_action_callbacks:
            try:
                cb(self, action, proxy, args)
            except:
                warnings.warn("Error occurred at pre action stage.\n{}".format(traceback.format_exc()))

    def post_action(self, action, proxy, args):
        for cb in self._post_action_callbacks:
            try:
                cb(self, action, proxy, args)
            except:
                warnings.warn("Error occurred at post action stage.\n{}".format(traceback.format_exc()))
