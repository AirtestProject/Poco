# coding=utf-8
__author__ = 'lxn3032'


import time

from airtest.core.main import touch, swipe, snapshot
from airtest.cli.runner import device as current_device
from airtest_hunter import AirtestHunter, open_platform
from poco import Poco
from poco.exceptions import InvalidOperationException
from hunter_rpc import HunterRpc


class AirtestPoco(Poco):
    def __init__(self, process, hunter=None):
        apitoken = open_platform.get_api_token(process)
        self._hunter = hunter or AirtestHunter(apitoken, process)
        rpc_client = HunterRpc(self._hunter)
        super(AirtestPoco, self).__init__(rpc_client)

        # 初始化时记录下来，不重复获取了
        self._screen_resolution = self.get_screen_size()
        self._touch_resolution = self.get_input_panel_size()

    def get_screen_size(self):
        return [float(s) for s in self.rpc.get_screen_size()]

    def get_input_panel_size(self):
        screen_w, screen_h = self.get_screen_size()
        display_info = current_device().get_display_info()
        real_w, real_h = display_info['width'], display_info['height']
        if screen_w > screen_h:
            w = max(real_w, real_h)
            h = min(real_w, real_h)
        else:
            w, h = real_w, real_h
        return [float(w), float(h)]  # 用于进行输入的分辨率，与设备输入接口对应

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        panel_size = self._touch_resolution
        pos = [pos[0] * panel_size[0], pos[1] * panel_size[1]]
        touch(pos)

    def swipe(self, p1, p2=None, direction=None, duration=1):
        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))
        panel_size = self._touch_resolution
        p1 = [p1[0] * panel_size[0], p1[1] * panel_size[1]]
        if p2:
            p2 = [p2[0] * panel_size[0], p2[1] * panel_size[1]]
        steps = int(duration * 40) + 1
        if not direction:
            swipe(p1, p2, duration=duration, steps=steps)
        else:
            swipe(p1, vector=direction, duration=duration, steps=steps)

    def snapshot(self, width):
        raise NotImplementedError

    def command(self, script, lang='text', sleep_interval=None):
        """
        通过hunter调用gm指令，可调用hunter指令库中定义的所有指令，也可以调用text类型的gm指令
        gm指令相关功能请参考safaia GM指令扩展模块

        :param script: 指令
        :param lang: 语言，默认text
        :param sleep_interval: 调用指令后的等待间隔时间
        :return: None
        """

        self._hunter.script(script, lang=lang)
        if sleep_interval:
            time.sleep(sleep_interval)
        else:
            self.wait_stable()
