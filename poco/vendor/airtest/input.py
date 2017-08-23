# coding=utf-8

from airtest.cli.runner import device as current_device
from airtest.core.main import touch, swipe
from poco.sdk.interfaces.input import InputInterface


class AirtestInput(InputInterface):
    def __init__(self):
        super(AirtestInput, self).__init__()

    def _get_touch_resolution(self):
        """get real time resolution on android"""
        size = current_device().display_info
        w, h = size["width"], size["height"]
        if size["orientation"] in (1, 3):
            return h, w
        else:
            return w, h

    def click(self, x, y):
        pw, ph = self._get_touch_resolution()
        pos = [x * pw, y * ph]
        touch(pos)

    def swipe(self, x1, y1, x2, y2, duration=2.0):
        direction = x2 - x1, y2 - y1
        pw, ph = self._get_touch_resolution()
        p1 = [x1 * pw, y1 * ph]
        steps = int(duration * 40) + 1
        swipe(p1, vector=direction, duration=duration, steps=steps)

    def longClick(self, x, y, duration=2.0):
        raise NotImplementedError
