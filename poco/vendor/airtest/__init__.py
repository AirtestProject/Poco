# coding=utf-8
__author__ = 'lxn3032'


from airtest.core.main import touch, swipe, snapshot
from airtest_hunter import AirtestHunter, open_platform
from poco import PocoUI


class AirtestPoco(PocoUI):
    def __init__(self, process, hunter=None):
        apitoken = open_platform.get_api_token()
        hunter = hunter or AirtestHunter(apitoken, process)
        super(AirtestPoco, self).__init__(hunter)

    def touch(self, pos):
        super(AirtestPoco, self).touch(pos)
        touch(pos)

    def swipe(self, p1, p2=None, direction=None, duration=1):
        super(AirtestPoco, self).swipe(p1, p2, direction, duration)
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
