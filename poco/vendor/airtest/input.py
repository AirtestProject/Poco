# coding=utf-8

import time

from poco.interfaces import InputInterface

from airtest.core.main import touch, swipe
from airtest.cli.runner import device as current_device


class AirtestInput(InputInterface):
    def __init__(self):
        super(AirtestInput, self).__init__()

    def _get_touch_resolution(self):
        """get real time resolution on android"""
        size = current_device().get_display_info()
        w, h = size["width"], size["height"]
        if size["orientation"] in (1, 3):
            return h, w
        else:
            return w, h

    def click(self, pos):
        panel_size = self._get_touch_resolution()
        pos = [pos[0] * panel_size[0], pos[1] * panel_size[1]]
        touch(pos)

    def swipe(self, p1, direction, duration=2.0):
        panel_size = self._get_touch_resolution()
        p1 = [p1[0] * panel_size[0], p1[1] * panel_size[1]]
        steps = int(duration * 40) + 1
        swipe(p1, vector=direction, duration=duration, steps=steps)

    def long_click(self, p, duration=2.0):
        raise NotImplementedError
