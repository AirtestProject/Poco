# coding=utf-8
__author__ = 'lxn3032'


from poco import Poco

from poco.exceptions import InvalidOperationException
from rpc import AndroidRpcClient


class AndroidUiautomationPoco(Poco):
    def __init__(self, serial):
        # TODO: android 初始化
        endpoint = "http://10.254.245.31:10081"
        rpc_client = AndroidRpcClient(endpoint)
        super(AndroidUiautomationPoco, self).__init__(rpc_client)

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        panel_size = self.screen_resolution
        pos = pos[0] * panel_size[0], pos[1] * panel_size[1]
        self.get_rpc_interface().click(*pos)

    def swipe(self, p1, p2=None, direction=None, duration=1):
        if not (0 <= p1[0] <= 1) or not (0 <= p1[1] <= 1):
            raise InvalidOperationException('Swipe origin out of screen. {}'.format(p1))
        panel_size = self.screen_resolution
        sp1 = [p1[0] * panel_size[0], p1[1] * panel_size[1]]
        if p2:
            sp2 = [p2[0] * panel_size[0], p2[1] * panel_size[1]]
        elif direction:
            sp2 = [(p1[0] + direction[0]) * panel_size[0], (p1[1] + direction[1]) * panel_size[1]]
        else:
            raise RuntimeError("p2 and direction cannot be None at the same time.")
        self.get_rpc_interface().swipe(sp1[0], sp1[1], sp2[0], sp2[1], duration)

    def long_click(self, pos, duration=2):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        panel_size = self.screen_resolution
        pos = int(pos[0] * panel_size[0]), int(pos[1] * panel_size[1])
        self.get_rpc_interface().long_click(pos[0], pos[1], duration)

    def snapshot(self, filename='sshot.png'):
        pass


import time
poco = AndroidUiautomationPoco("")
print poco.get_rpc_interface().remote_poco.dump()

# print poco('android:id/action_bar').get_bounds()
# print poco(text='更多').drag_to(poco(text='WLAN'))
# poco(text='WLAN').click()
# poco(text='netease_game').click()
# poco(text='完成').click()