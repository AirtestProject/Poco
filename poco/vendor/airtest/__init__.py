# coding=utf-8
__author__ = 'lxn3032'


from airtest.core.main import touch, swipe, snapshot
from airtest.cli.runner import device as current_device
from airtest_hunter import AirtestHunter, open_platform
from poco import Poco
from poco.exceptions import InvalidOperationException


class AirtestPoco(Poco):
    def __init__(self, process, hunter=None):
        apitoken = open_platform.get_api_token(process)
        hunter = hunter or AirtestHunter(apitoken, process)
        super(AirtestPoco, self).__init__(hunter)

    def _init_screen_info(self):
        # override
        engine_w, engine_h = self.remote_poco.get_screen_size()
        display_info = current_device().get_display_info()
        real_w, real_h = display_info['width'], display_info['height']
        if engine_w > engine_h:
            w = max(real_w, real_h)
            h = min(real_w, real_h)
        else:
            w, h = real_w, real_h
        self.screen_resolution = [float(w), float(h)]

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        screen_size = self.screen_resolution
        pos = [pos[0] * screen_size[0], pos[1] * screen_size[1]]
        touch(pos)

    def swipe(self, p1, p2=None, direction=None, duration=1):
        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))
        screen_size = self.screen_resolution
        p1 = [p1[0] * screen_size[0], p1[1] * screen_size[1]]
        if p2:
            p2 = [p2[0] * screen_size[0], p2[1] * screen_size[1]]
        steps = int(duration * 40) + 1
        if not direction:
            swipe(p1, p2, duration=duration, steps=steps)
        else:
            swipe(p1, vector=direction, duration=duration, steps=steps)

    def snapshot(self, filename='sshot.png'):
        # windows系统文件名最大长度有限制
        if len(filename) > 220:
            filename = filename[:220]
        if not filename.endswith('.png'):
            filename += '.png'
        snapshot(filename)
