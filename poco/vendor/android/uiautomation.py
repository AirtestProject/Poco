# coding=utf-8
__author__ = 'lxn3032'


from poco import Poco

from poco.exceptions import InvalidOperationException
from rpc import AndroidRpcClient


class AndroidUiautomationPoco(Poco):
    def __init__(self, serial):
        endpoint = "http://10.254.245.31:10081"
        rpc_client = AndroidRpcClient(endpoint)
        super(AndroidUiautomationPoco, self).__init__(rpc_client)

    def click(self, pos):
        if not (0 <= pos[0] <= 1) or not (0 <= pos[1] <= 1):
            raise InvalidOperationException('Click position out of screen. {}'.format(pos))
        panel_size = self.screen_resolution
        pos = int(pos[0] * panel_size[0]), int(pos[1] * panel_size[1])
        self._rpc_client.remote_poco.inputer.click(*pos)

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

        # 目标设备duration以毫秒为单位
        self._rpc_client.remote_poco.inputer.swipe(int(sp1[0]), int(sp1[1]), int(sp2[0]), int(sp2[1]), int(duration * 1000))

    def snapshot(self, filename='sshot.png'):
        pass
        # windows系统文件名最大长度有限制
        # if len(filename) > 220:
        #     filename = filename[:220]
        # if not filename.endswith('.png'):
        #     filename += '.png'
        # snapshot(filename)


poco = AndroidUiautomationPoco("")
# print poco._rpc_client.remote_poco.dumper.dumpHierarchy()
# print poco._rpc_client.remote_poco.selector.select(["and",[["attr=",["text","WLAN"]]]])
# print poco('android:id/action_bar').get_bounds()
print poco(text='更多').drag_to(poco(text='WLAN'))