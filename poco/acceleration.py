# coding=utf-8
__author__ = 'lxn3032'


import time

from .exceptions import PocoTargetTimeout


class PocoUIAccelerationMixin(object):
    """
    该mixin中定义一些常用的操作方法，将一些通用的逻辑封装起来。
    """

    def dismiss(self, targets, exit_when=None, anchor='anchor', sleep_interval=1, appearance_timeout=20, timeout=120):
        """
        自动点掉目标对象，即一直点点到全都消失为止，适用于无脑点点点的界面。

        :param targets: <list> 目标对象列表，poco选择的对象
        :param exit_when: 结束条件，默认为targets中所有节点都消失后自动退出
        :param anchor: 点击对象的局部坐标系位置，默认点击anchor点。
        :param sleep_interval: 点击动作间隔，点了之后等待一段时间后再找下一个target进行点击
        :param appearance_timeout: 在进行dismiss之前会等待targets中任意一个target出现，超过了这个时间还没出现就自动退出了
        :param timeout: dismiss阶段超时时长
        :return: None
        """
        try:
            self.wait_for_any(targets, timeout=appearance_timeout)
        except PocoTargetTimeout:
            # 仅当超时时自动退出
            return

        start_time = time.time()
        while True:
            no_target = True
            for t in targets:
                if t.exists():
                    try:
                        t.click(anchor=anchor, sleep_interval=sleep_interval)
                        no_target = False
                    except:
                        pass
            time.sleep(sleep_interval)
            should_exit = exit_when() if exit_when else False
            if no_target or should_exit or time.time() - start_time > timeout:
                return
