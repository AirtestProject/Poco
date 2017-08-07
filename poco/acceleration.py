# coding=utf-8
from __future__ import unicode_literals

import time
import warnings

from .exceptions import PocoTargetTimeout

__author__ = 'lxn3032'


class PocoAccelerationMixin(object):
    """
    该mixin中定义一些常用的操作方法，将一些通用的逻辑封装起来。
    """

    def dismiss(self, targets, exit_when=None, sleep_interval=0.5, appearance_timeout=20, timeout=120):
        """
        自动点掉目标对象，即一直点点到全都消失为止，适用于无脑点点点的界面。

        :param targets: <list> 目标对象列表，poco选择的对象
        :param exit_when: 结束条件，默认为targets中所有节点都消失后自动退出
        :param sleep_interval: 点击动作间隔，点了之后等待一段时间后再找下一个target进行点击
        :param appearance_timeout: 在进行dismiss之前会等待targets中任意一个target出现，超过了这个时间还没出现就自动退出了
        :param timeout: dismiss阶段超时时长
        :return: None

        :raise PocoTargetTimeout: 当处于dismiss切超时时，会报这个错，因为正常情况下不可能这么长时间还没把该消的消掉
        """

        try:
            self.wait_for_any(targets, timeout=appearance_timeout)
        except PocoTargetTimeout:
            # 仅当超时时自动退出
            warnings.warn('尝试dismiss前等待对象出现但超时 {}'.encode('utf-8').format(targets))
            return

        start_time = time.time()
        while True:
            no_target = True
            for t in targets:
                if t.exists():
                    for n in t:
                        try:
                            n.click(sleep_interval=sleep_interval)
                            no_target = False
                        except:
                            pass
            time.sleep(sleep_interval)
            should_exit = exit_when() if exit_when else False
            if no_target or should_exit:
                return

            if time.time() - start_time > timeout:
                raise PocoTargetTimeout('dismiss', repr(targets).decode('utf-8'))
